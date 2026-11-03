from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database import get_session
from app.models import Property
from app.demo_state import (
    NEGOTIATIONS,
    TENANT_RENTED_OR_BOUGHT,
    get_cart_ids,
    get_current_user,
    get_effective_base_price,
    set_flash_message,
)
from app.template_utils import render_page

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _build_cart_items(session: Session, cart_ids: list[int]) -> tuple[list[dict], int, int]:
    items = []
    grand_total = 0
    total_savings = 0
    for pid in cart_ids:
        prop = session.get(Property, pid)
        if not prop:
            continue
        effective_base = get_effective_base_price(prop)
        savings = max(0, prop.base_price - effective_base)
        item_total = effective_base + prop.additional_charges_total
        grand_total += item_total
        total_savings += savings
        items.append(
            {
                "property": prop,
                "effective_base_price": effective_base,
                "is_negotiated_discount": savings > 0,
                "savings": savings,
                "item_total": item_total,
            }
        )
    return items, grand_total, total_savings


@router.get("/negotiate/{property_id}")
def deal_room_page(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    """08 Transaction-support service: Structured Offer & Counter-Offer Timeline ('Deal Room')."""
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    user = get_current_user(request)
    neg = NEGOTIATIONS.get(property_id)

    if not neg and prop.is_negotiable:
        neg = {
            "property_id": prop.id,
            "property_title": prop.title,
            "tenant_name": user["name"],
            "landlord_name": prop.landlord_name,
            "listed_price": prop.base_price,
            "current_agreed_price": prop.base_price,
            "status": "Open for Structured Offer",
            "payment_tenure": "1 Year Annual Lease" if prop.category == "Rent" else "Outright Settlement",
            "move_in_target": "Within 14 Days",
            "events": [
                {
                    "step": "01",
                    "actor": "Estate Deal Room",
                    "role": "system",
                    "badge": "Negotiation Enabled",
                    "proposed_price": prop.base_price,
                    "note": (
                        f"Direct Landlord ({prop.landlord_name}) has authorized structured negotiation for "
                        f"{prop.title}. Submit a proposed offer below."
                    ),
                    "timestamp": "Just now",
                }
            ],
        }
        NEGOTIATIONS[property_id] = neg

    effective_base = neg["current_agreed_price"] if neg else prop.base_price
    negotiated_total = effective_base + prop.additional_charges_total

    return render_page(
        request,
        "transactions/negotiate.html",
        {
            "property": prop,
            "negotiation": neg,
            "effective_base": effective_base,
            "negotiated_total": negotiated_total,
            "potential_savings": max(0, prop.base_price - effective_base),
        },
    )


@router.post("/negotiate/{property_id}/offer")
def submit_structured_offer(
    request: Request,
    property_id: int,
    proposed_price: int = Form(...),
    payment_tenure: str = Form("1 Year Annual Lease"),
    move_in_target: str = Form("Within 14 Days"),
    note: str = Form("Ready to proceed with Estate Escrow checkout upon approval."),
    actor_mode: str = Form("tenant"),  # "tenant" or "landlord"
    session: Session = Depends(get_session),
):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    if not prop.is_negotiable:
        set_flash_message(request, "This property has a fixed non-negotiable price set by the landlord.", "warning")
        return RedirectResponse(url=f"/properties/{property_id}", status_code=303)

    user = get_current_user(request)
    neg = NEGOTIATIONS.get(property_id)
    if not neg:
        neg = {
            "property_id": prop.id,
            "property_title": prop.title,
            "tenant_name": user["name"],
            "landlord_name": prop.landlord_name,
            "listed_price": prop.base_price,
            "current_agreed_price": proposed_price,
            "status": "Offer Sent",
            "payment_tenure": payment_tenure,
            "move_in_target": move_in_target,
            "events": [],
        }
        NEGOTIATIONS[property_id] = neg

    step_num = f"{len(neg['events']) + 1:02d}"
    is_landlord = actor_mode == "landlord" or user["role"] == "landlord"

    neg["payment_tenure"] = payment_tenure
    neg["move_in_target"] = move_in_target
    neg["current_agreed_price"] = proposed_price

    if is_landlord:
        neg["status"] = "Counter-Offer Active"
        neg["events"].append(
            {
                "step": step_num,
                "actor": f"{prop.landlord_name} (Landlord)",
                "role": "landlord",
                "badge": "Landlord Counter-Offer",
                "proposed_price": proposed_price,
                "note": note,
                "timestamp": "Just now",
            }
        )
        set_flash_message(request, f"Landlord counter-offer of ₦{proposed_price:,} posted to Deal Room.", "info")
    else:
        neg["events"].append(
            {
                "step": step_num,
                "actor": f"{user['name']} (Tenant)",
                "role": "tenant",
                "badge": f"Structured Offer ({payment_tenure})",
                "proposed_price": proposed_price,
                "note": note,
                "timestamp": "Just now",
            }
        )
        # Smart instant landlord feedback if offer meets landlord's minimum acceptable price
        if proposed_price >= prop.min_acceptable_price:
            step_next = f"{len(neg['events']) + 1:02d}"
            neg["status"] = "Accepted"
            neg["events"].append(
                {
                    "step": step_next,
                    "actor": f"{prop.landlord_name} (Landlord Auto-Mandate)",
                    "role": "landlord",
                    "badge": "Offer Accepted ✓",
                    "proposed_price": proposed_price,
                    "note": (
                        f"Your offer of ₦{proposed_price:,} meets the landlord's pre-authorized settlement range! "
                        "Price is now locked for your checkout."
                    ),
                    "timestamp": "Instant Mandate Match",
                }
            )
            set_flash_message(
                request,
                f"Offer of ₦{proposed_price:,} accepted! Your negotiated price is locked for checkout.",
                "success",
            )
        else:
            # Landlord counter-offers halfway between min_acceptable_price and listed base_price
            counter_val = max(prop.min_acceptable_price, int((proposed_price + prop.base_price) / 2))
            neg["current_agreed_price"] = counter_val
            neg["status"] = "Counter-Offer Active"
            step_next = f"{len(neg['events']) + 1:02d}"
            neg["events"].append(
                {
                    "step": step_next,
                    "actor": f"{prop.landlord_name} (Landlord)",
                    "role": "landlord",
                    "badge": "Landlord Counter-Offer",
                    "proposed_price": counter_val,
                    "note": (
                        f"Thank you for your offer of ₦{proposed_price:,}. Given the verified infrastructure and "
                        f"recent upgrades, I can meet you at ₦{counter_val:,}."
                    ),
                    "timestamp": "Moment ago",
                }
            )
            set_flash_message(
                request,
                f"Offer submitted! Landlord responded with a structured counter-offer of ₦{counter_val:,}.",
                "info",
            )

    return RedirectResponse(url=f"/transactions/negotiate/{property_id}", status_code=303)


@router.post("/negotiate/{property_id}/accept")
def accept_negotiation_offer(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    prop = session.get(Property, property_id)
    neg = NEGOTIATIONS.get(property_id)
    if not prop or not neg:
        raise HTTPException(status_code=404, detail="Negotiation not found")

    neg["status"] = "Accepted"
    step_num = f"{len(neg['events']) + 1:02d}"
    neg["events"].append(
        {
            "step": step_num,
            "actor": "Deal Room Escrow Lock",
            "role": "system",
            "badge": "Deal Locked ✓",
            "proposed_price": neg["current_agreed_price"],
            "note": f"Both parties agreed on ₦{neg['current_agreed_price']:,}. Property added to checkout tray.",
            "timestamp": "Just now",
        }
    )

    cart_ids = get_cart_ids(request)
    if property_id not in cart_ids:
        cart_ids.append(property_id)
        request.session["cart_ids"] = cart_ids

    set_flash_message(
        request,
        f"Deal locked at ₦{neg['current_agreed_price']:,}! Added '{prop.title}' to your checkout tray.",
        "success",
    )
    return RedirectResponse(url="/transactions/cart", status_code=303)


@router.get("/cart")
def view_cart(request: Request, session: Session = Depends(get_session)):
    cart_ids = get_cart_ids(request)
    items, grand_total, total_savings = _build_cart_items(session, cart_ids)

    # Also pass available properties not yet in cart so tenant can easily select multiple properties
    from sqlmodel import select
    other_available = [
        p
        for p in session.exec(select(Property).where(Property.status == "Available")).all()
        if p.id not in cart_ids
    ]

    return render_page(
        request,
        "transactions/cart.html",
        {
            "cart_items": items,
            "grand_total": grand_total,
            "total_savings": total_savings,
            "other_available": other_available,
        },
    )


@router.post("/cart/add/{property_id}")
def add_to_cart(
    request: Request,
    property_id: int,
    redirect_to: str = Form("/transactions/cart"),
    session: Session = Depends(get_session),
):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    cart_ids = list(get_cart_ids(request))
    if property_id not in cart_ids:
        cart_ids.append(property_id)
        request.session["cart_ids"] = cart_ids
        set_flash_message(request, f"Added '{prop.title}' to your property selection tray.", "success")
    else:
        set_flash_message(request, f"'{prop.title}' is already in your checkout tray.", "info")

    return RedirectResponse(url=redirect_to, status_code=303)


@router.post("/cart/remove/{property_id}")
def remove_from_cart(request: Request, property_id: int):
    cart_ids = [pid for pid in get_cart_ids(request) if pid != property_id]
    request.session["cart_ids"] = cart_ids
    set_flash_message(request, "Removed property from your checkout tray.", "info")
    return RedirectResponse(url="/transactions/cart", status_code=303)


@router.get("/checkout")
def checkout_gateway_page(request: Request, session: Session = Depends(get_session)):
    cart_ids = get_cart_ids(request)
    items, grand_total, total_savings = _build_cart_items(session, cart_ids)

    return render_page(
        request,
        "transactions/checkout.html",
        {
            "cart_items": items,
            "grand_total": grand_total,
            "total_savings": total_savings,
            "receipt": None,
        },
    )


@router.post("/checkout/pay")
def process_payment_gateway(
    request: Request,
    payment_method: str = Form("Estate Escrow Card"),
    payer_name: str = Form("Chidi Nwosu"),
    payer_email: str = Form("tenant@estate.ng"),
    session: Session = Depends(get_session),
):
    """
    Processes multi-property checkout:
    1. Marks purchased/rented properties as 'Unavailable' in SQLite (Feature 03)
    2. Adds them to the Tenant's Rented/Bought portfolio so they can review them on the Tenant Dashboard
    3. Renders an official Estate Escrow Receipt
    """
    cart_ids = get_cart_ids(request)
    items, grand_total, total_savings = _build_cart_items(session, cart_ids)

    if not items:
        set_flash_message(request, "Your property checkout tray is empty.", "warning")
        return RedirectResponse(url="/properties", status_code=303)

    tx_ref = f"EST-ESCROW-{int(datetime.now().timestamp()) % 900000 + 100000}"
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    settled_titles = []
    for item in items:
        prop: Property = item["property"]
        prop.status = "Unavailable"
        session.add(prop)
        settled_titles.append(prop.title)

        TENANT_RENTED_OR_BOUGHT.insert(
            0,
            {
                "transaction_id": tx_ref,
                "property_id": prop.id,
                "property_title": prop.title,
                "property_location": prop.location,
                "property_image": prop.image_url,
                "category": prop.category,
                "landlord_name": prop.landlord_name,
                "amount_paid": item["item_total"],
                "date_completed": datetime.now().strftime("%d %b %Y"),
                "payment_method": payment_method,
                "my_property_rating": 0,
                "my_property_review": "",
            },
        )

    session.commit()
    request.session["cart_ids"] = []

    receipt = {
        "tx_ref": tx_ref,
        "date_str": date_str,
        "payer_name": payer_name,
        "payer_email": payer_email,
        "payment_method": payment_method,
        "settled_items": items,
        "grand_total": grand_total,
        "total_savings": total_savings,
        "settled_count": len(items),
    }

    set_flash_message(
        request,
        f"Payment of ₦{grand_total:,} confirmed! {len(items)} property(s) marked 'Unavailable' and added to your Tenant Dashboard.",
        "success",
    )

    return render_page(
        request,
        "transactions/checkout.html",
        {
            "cart_items": items,
            "grand_total": grand_total,
            "total_savings": total_savings,
            "receipt": receipt,
        },
    )
