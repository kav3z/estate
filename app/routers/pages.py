from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Property
from app.demo_state import (
    NEIGHBOURHOODS,
    RESIDENT_FEEDBACK,
    PLATFORM_REVIEWS,
    FAQS,
    SUPPORT_TICKETS,
    ACCOUNTABILITY_COMPLAINTS,
    get_current_user,
    set_flash_message,
)
from app.template_utils import render_page

router = APIRouter(tags=["pages"])


@router.get("/")
def landing_page(request: Request, session: Session = Depends(get_session)):
    all_props = list(session.exec(select(Property).order_by(Property.id.asc())).all())
    featured_props = [p for p in all_props if p.status == "Available"][:4]

    counts = {
        "total_units": len(all_props),
        "verified_units": sum(1 for p in all_props if p.is_verified),
        "houses": sum(1 for p in all_props if p.property_type in ("Duplex", "Bungalow")),
        "apartments": sum(1 for p in all_props if p.property_type == "Apartment"),
        "lands": sum(1 for p in all_props if p.property_type == "Land"),
    }

    return render_page(
        request,
        "index.html",
        {
            "properties": all_props[:6],
            "featured_props": featured_props,
            "counts": counts,
            "neighbourhoods": list(NEIGHBOURHOODS.values())[:4],
            "platform_reviews": PLATFORM_REVIEWS[:3],
            "complaints_preview": ACCOUNTABILITY_COMPLAINTS[:2],
        },
    )


@router.get("/neighbourhoods")
def neighbourhoods_page(
    request: Request,
    area: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """Neighbourhood Intelligence & Verified Paid-Tenant Resident Feedback."""
    selected_key = area if area in NEIGHBOURHOODS else "maitama-abuja"
    selected_area = NEIGHBOURHOODS[selected_key]

    feedback_list = [
        fb for fb in RESIDENT_FEEDBACK if not area or fb["neighbourhood_key"] == selected_key
    ]
    area_properties = list(
        session.exec(
            select(Property).where(Property.neighbourhood_key == selected_key)
        ).all()
    )

    return render_page(
        request,
        "community/neighbourhoods.html",
        {
            "neighbourhoods": list(NEIGHBOURHOODS.values()),
            "selected_area": selected_area,
            "selected_key": selected_key,
            "feedback_list": feedback_list,
            "area_properties": area_properties,
            "all_feedback": RESIDENT_FEEDBACK,
        },
    )


@router.post("/neighbourhoods/feedback")
def submit_resident_feedback(
    request: Request,
    neighbourhood_key: str = Form(...),
    resident_name: str = Form(...),
    residency_duration: str = Form("2 Years Verified Resident"),
    rating: int = Form(5),
    power_report: str = Form(...),
    water_report: str = Form(...),
    drainage_report: str = Form(...),
    comment: str = Form(...),
):
    new_fb = {
        "id": len(RESIDENT_FEEDBACK) + 1,
        "neighbourhood_key": neighbourhood_key,
        "resident_name": resident_name.strip(),
        "residency_duration": residency_duration.strip(),
        "verification_badge": "Utility & Residency Verified",
        "rating": max(1, min(5, rating)),
        "power_report": power_report.strip(),
        "water_report": water_report.strip(),
        "drainage_report": drainage_report.strip(),
        "comment": comment.strip(),
        "created_at": "Just now",
    }
    RESIDENT_FEEDBACK.insert(0, new_fb)
    set_flash_message(
        request,
        f"Verified resident intelligence added for {NEIGHBOURHOODS.get(neighbourhood_key, {}).get('name', neighbourhood_key)}!",
        "success",
    )
    return RedirectResponse(url=f"/neighbourhoods?area={neighbourhood_key}", status_code=303)


@router.get("/reviews")
def reviews_page(request: Request):
    """06 Review: Where tenants rate and say how the platform has been of good use to them."""
    return render_page(
        request,
        "community/reviews.html",
        {
            "platform_reviews": PLATFORM_REVIEWS,
        },
    )


@router.post("/reviews/add")
def submit_platform_review(
    request: Request,
    rating: int = Form(5),
    impact_tag: str = Form("Transparent Fees & Verified Landlord"),
    property_ref: str = Form("General Platform Experience"),
    comment: str = Form(...),
    redirect_to: str = Form("/reviews"),
):
    user = get_current_user(request)
    new_rev = {
        "id": len(PLATFORM_REVIEWS) + 1,
        "user_name": user["name"],
        "user_role": f"Verified {user['role'].capitalize()}",
        "user_avatar": user["avatar"],
        "rating": max(1, min(5, rating)),
        "impact_tag": impact_tag.strip(),
        "property_ref": property_ref.strip(),
        "comment": comment.strip(),
        "date": "Just now",
    }
    PLATFORM_REVIEWS.insert(0, new_rev)
    set_flash_message(request, "Thank you! Your Estate platform review is now live.", "success")
    return RedirectResponse(url=redirect_to, status_code=303)


@router.get("/help")
def help_faq_contact_page(request: Request):
    """07 HELP: FAQ page and Contact Us page."""
    return render_page(
        request,
        "community/help.html",
        {
            "faqs": FAQS,
            "support_tickets": SUPPORT_TICKETS,
        },
    )


@router.post("/help/contact")
def submit_contact_ticket(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    topic: str = Form("Verification & Property Enquiry"),
    message: str = Form(...),
):
    ticket_id = f"HLP-{900 + len(SUPPORT_TICKETS) + 1}"
    SUPPORT_TICKETS.insert(
        0,
        {
            "ticket_id": ticket_id,
            "name": name.strip(),
            "email": email.strip(),
            "topic": topic.strip(),
            "message": message.strip(),
            "status": "Received — Assigned to Estate Trust Desk (< 2hr SLA)",
            "created_at": "Just now",
        },
    )
    set_flash_message(
        request,
        f"Support ticket {ticket_id} submitted! Our team will respond to {email} shortly.",
        "success",
    )
    return RedirectResponse(url="/help", status_code=303)


@router.post("/api/chatbot")
async def estate_ai_chatbot(
    request: Request,
    session: Session = Depends(get_session),
):
    """
    AI Assistant endpoint for the bottom-right Estate Chatbot widget.
    Answers questions about live property listings, land plots, transparent charges,
    neighbourhood power/drainage, Deal Room negotiation, and support issues.
    """
    payload = await request.json()
    user_msg = (payload.get("message") or "").strip()
    lower_msg = user_msg.lower()

    all_props = list(session.exec(select(Property)).all())
    available_props = [p for p in all_props if p.status == "Available"]

    # 1. Check if user is asking about land
    if any(k in lower_msg for k in ["land", "plot", "sqm", "katampe", "lugbe", "acre", "c of o", "r of o", "tdp"]):
        lands = [p for p in all_props if p.property_type == "Land"]
        lines = [
            f"• **{p.title}** ({p.location}) — **{p.size_sqm} m²**, Stated Price: **₦{p.base_price:,}** (5% Agency Fee + C of O + R of O + TDP included • Full Commitment: **₦{p.total_initial_commitment:,}**). [View Plot](/properties/{p.id})"
            for p in lands
        ]
        reply = (
            "Here are our verified dry **Serviced Land Plots** on Estate (including complete **C of O**, **R of O**, and **TDP** documentation breakdown and a **5% Land Sale Agency Fee**):\n\n"
            + "\n".join(lines)
        )
        return {"reply": reply, "suggestions": ["How does negotiation work?", "Check Maitama power hours", "View all properties"]}

    # 2. Check if user is asking about houses, rent, duplex, bungalow, apartment, or listings
    if any(k in lower_msg for k in ["rent", "buy", "house", "duplex", "bungalow", "apartment", "listing", "available", "property", "properties", "cheapest", "price", "abuja"]):
        sample = available_props[:4]
        lines = [
            f"• **{p.title}** ({p.category} • {p.property_type} in {p.location}) — Base: **₦{p.base_price:,}**, Full Commitment: **₦{p.total_initial_commitment:,}** ({'Negotiable' if p.is_negotiable else 'Fixed'}). [Inspect](/properties/{p.id})"
            for p in sample
        ]
        reply = (
            f"We currently have **{len(available_props)} verified available listings** across Abuja (Maitama, Asokoro, Wuse II, Guzape, Jabi, Katampe, Airport Road) and Lagos on Estate:\n\n"
            + "\n".join(lines)
            + "\n\nWould you like me to match you by budget or bedroom count?"
        )
        return {"reply": reply, "suggestions": ["Open Smart Matcher", "Show land listings", "What are transparent charges?"]}

    # 3. Check if user is asking about fees, charges, commitment, agency, caution, or escrow
    if any(k in lower_msg for k in ["fee", "charge", "cost", "commitment", "agency", "legal", "caution", "escrow", "pay", "checkout"]):
        reply = (
            "**Transparent Charges & Escrow Protection on Estate:**\n\n"
            "1. **Standardized Agency Fees**: **7%** for houses/apartments and **5%** for land sales.\n"
            "2. **Land Statutory Documents Included**: Every land plot breakdown explicitly itemizes **C of O** (Certificate of Occupancy), **R of O** (Right of Occupancy), and **TDP** (Title Deed Plan).\n"
            "3. **Estate Escrow Checkout**: When you pay at `/transactions/checkout`, your money is held safely in our Escrow Vault until keys or land documents are physically handed over."
        )
        return {"reply": reply, "suggestions": ["Open Checkout Tray", "How does Deal Room negotiation work?", "Contact Support"]}

    # 4. Check if user is asking about negotiation / deal room
    if any(k in lower_msg for k in ["negotiate", "negotiation", "deal room", "offer", "discount", "bargain"]):
        neg_props = [p for p in available_props if p.is_negotiable]
        reply = (
            f"**Structured Deal Room Negotiation:**\n\n"
            f"When a landlord enables negotiation (currently **{len(neg_props)} listings** allow this), you can open the **Deal Room** on the property page to propose a price with a live slider and choose your payment tenure. If your offer meets the landlord's pre-authorized floor, it locks immediately for checkout!"
        )
        return {"reply": reply, "suggestions": ["Try Deal Room on Serenity Pines", "Show available properties", "How does verification work?"]}

    # 5. Check if user is asking about neighbourhood power, light, water, drainage, flood, security
    if any(k in lower_msg for k in ["power", "light", "electricity", "water", "drainage", "flood", "security", "neighbourhood", "area", "lekki", "ikoyi", "ikeja", "yaba", "maitama"]):
        reply = (
            "**Neighbourhood Intelligence Summary:**\n\n"
            "• **Old Ikoyi**: 24 hrs/day power • 9.8/10 Flood-Free Drainage • 9.9/10 Security\n"
            "• **Maitama, Abuja**: 23 hrs/day power • 9.7/10 Drainage • 9.8/10 Security\n"
            "• **Lekki Phase 1**: 22 hrs/day power • 9.2/10 Drainage • 9.7/10 Security\n"
            "• **Ikeja GRA**: 21 hrs/day power • 9.5/10 Upland Drainage • 9.6/10 Security\n\n"
            "You can also read and post **Verified Resident Feedback** at [Neighbourhood Intel](/neighbourhoods)."
        )
        return {"reply": reply, "suggestions": ["Explore Neighbourhood Intel", "Show properties in Lekki", "Book an inspection"]}

    # 6. Check if user has an issue, complaint, fake agent, or help question
    if any(k in lower_msg for k in ["issue", "problem", "help", "support", "complaint", "fake", "scam", "verify", "verification", "7-day", "unavailable", "dashboard"]):
        reply = (
            "**How Estate Protects You & Resolves Issues:**\n\n"
            "• **Verified Listings**: Every landlord/agent's C of O or Mandate is verified before publishing.\n"
            "• **7-Day Rule**: Landlords reconfirm availability every 7 days on their dashboard.\n"
            "• **Accountability & Support**: You can file a formal dispute on your [Tenant Dashboard](/dashboard/tenant) or submit a direct ticket on our [Help & FAQ page](/help)."
        )
        return {"reply": reply, "suggestions": ["Go to Help & Contact Page", "Open Tenant Dashboard", "Open Landlord Dashboard"]}

    # Default helpful concierge response
    reply = (
        f"Hello **{get_current_user(request)['name']}**! I'm your **Estate AI Concierge**. "
        f"We currently have **{len(available_props)} verified houses and land plots** ready for inspection or checkout.\n\n"
        "Ask me about **available properties**, **serviced land plots**, **upfront rental charges**, **neighbourhood power & drainage**, **Deal Room negotiation**, or **how to resolve an issue**!"
    )
    return {
        "reply": reply,
        "suggestions": [
            "Show available properties",
            "Show serviced land plots",
            "How do transparent charges work?",
            "I need help with an issue",
        ],
    }


