from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, Request, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Property
from app.demo_state import (
    NEIGHBOURHOODS,
    RESIDENT_FEEDBACK,
    NEGOTIATIONS,
    INSPECTIONS_AND_APPLICATIONS,
    TENANT_RENTED_OR_BOUGHT,
    get_current_user,
    has_user_paid_for_property,
    set_flash_message,
)
from app.template_utils import render_page

router = APIRouter(tags=["properties"])

UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f"{slug}-{int(datetime.now().timestamp()) % 10000}"


@router.get("/properties")
def list_properties(
    request: Request,
    category: Optional[str] = None,
    property_type: Optional[str] = None,
    location: Optional[str] = None,
    max_price: Optional[int] = None,
    verified_only: Optional[bool] = False,
    available_only: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    query = select(Property).order_by(Property.id.desc())
    all_props = list(session.exec(query).all())

    filtered = []
    for p in all_props:
        if category and category != "All" and p.category.lower() != category.lower():
            continue
        if property_type and property_type != "All" and p.property_type.lower() != property_type.lower():
            continue
        if location and location != "All" and location.lower() not in p.location.lower():
            continue
        if max_price and max_price > 0 and p.base_price > max_price:
            continue
        if verified_only and not p.is_verified:
            continue
        if available_only and p.status != "Available":
            continue
        filtered.append(p)

    counts = {
        "total": len(all_props),
        "houses": sum(1 for p in all_props if p.property_type in ("Duplex", "Bungalow")),
        "apartments": sum(1 for p in all_props if p.property_type == "Apartment"),
        "lands": sum(1 for p in all_props if p.property_type == "Land"),
    }

    return render_page(
        request,
        "properties/list.html",
        {
            "properties": filtered,
            "counts": counts,
            "filters": {
                "category": category or "All",
                "property_type": property_type or "All",
                "location": location or "All",
                "max_price": max_price or "",
                "verified_only": verified_only,
                "available_only": available_only,
            },
        },
    )


@router.get("/properties/{property_id}")
def property_detail(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    neighbourhood = NEIGHBOURHOODS.get(
        prop.neighbourhood_key,
        list(NEIGHBOURHOODS.values())[0],
    )
    area_feedback = [
        fb for fb in RESIDENT_FEEDBACK if fb["neighbourhood_key"] == prop.neighbourhood_key
    ]
    negotiation = NEGOTIATIONS.get(prop.id)
    is_paid_tenant = has_user_paid_for_property(prop.id)

    similar = list(
        session.exec(
            select(Property).where(Property.id != prop.id).limit(3)
        ).all()
    )

    return render_page(
        request,
        "properties/detail.html",
        {
            "property": prop,
            "neighbourhood": neighbourhood,
            "area_feedback": area_feedback,
            "negotiation": negotiation,
            "is_paid_tenant": is_paid_tenant,
            "similar_properties": similar,
        },
    )


@router.post("/properties/{property_id}/area-review")
def submit_paid_tenant_area_review(
    request: Request,
    property_id: int,
    rating: int = Form(5),
    power_report: str = Form("22 hrs/day verified"),
    water_report: str = Form("Clean treated water"),
    drainage_report: str = Form("Flood-free drainage"),
    comment: str = Form(...),
    session: Session = Depends(get_session),
):
    """
    Allows an already paid tenant/buyer to submit a review of a property and its area
    directly on the property page, and automatically publishes it to Neighbourhood Intel.
    """
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    if not has_user_paid_for_property(prop.id):
        set_flash_message(
            request,
            "Only verified tenants/buyers who have completed payment for this property can post an area review.",
            "warning",
        )
        return RedirectResponse(url=f"/properties/{property_id}", status_code=303)

    user = get_current_user(request)
    new_fb = {
        "id": len(RESIDENT_FEEDBACK) + 1,
        "property_id": prop.id,
        "property_title": prop.title,
        "neighbourhood_key": prop.neighbourhood_key,
        "resident_name": user["name"],
        "residency_duration": f"Verified Paid {'Buyer' if prop.category == 'Buy' else 'Tenant'} ({prop.title})",
        "verification_badge": "Escrow Payment & Tenancy Verified",
        "rating": max(1, min(5, rating)),
        "power_report": power_report.strip(),
        "water_report": water_report.strip(),
        "drainage_report": drainage_report.strip(),
        "comment": comment.strip(),
        "created_at": "Just now",
    }
    RESIDENT_FEEDBACK.insert(0, new_fb)

    # Also update the tenant's portfolio review if present
    for tx in TENANT_RENTED_OR_BOUGHT:
        if tx["property_id"] == prop.id:
            tx["my_property_rating"] = max(1, min(5, rating))
            tx["my_property_review"] = comment.strip()
            break

    nb_name = NEIGHBOURHOODS.get(prop.neighbourhood_key, {}).get("name", prop.location)
    set_flash_message(
        request,
        f"Your verified review for '{prop.title}' and '{nb_name}' is now live on this page and in Neighbourhood Intel!",
        "success",
    )
    return RedirectResponse(url=f"/properties/{property_id}#area-intel-reviews", status_code=303)


@router.post("/properties/{property_id}/book-inspection")
def book_inspection(
    request: Request,
    property_id: int,
    preferred_date: str = Form(...),
    preferred_time: str = Form("11:00 AM"),
    inspection_type: str = Form("Physical On-Site Viewing"),
    note: str = Form("Confirmed transparent rental/purchase charges upfront."),
    session: Session = Depends(get_session),
):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    user = get_current_user(request)
    new_booking = {
        "id": f"INSP-{500 + len(INSPECTIONS_AND_APPLICATIONS) + 1}",
        "property_id": prop.id,
        "property_title": prop.title,
        "location": prop.location,
        "applicant_name": user["name"],
        "applicant_score": f"{user['reputation_score']}★ Verified {user['role'].capitalize()}",
        "preferred_date": preferred_date,
        "preferred_time": preferred_time,
        "inspection_type": inspection_type,
        "application_status": "Inspection Confirmed",
        "note": note,
    }
    INSPECTIONS_AND_APPLICATIONS.insert(0, new_booking)
    set_flash_message(
        request,
        f"Inspection {new_booking['id']} scheduled for {prop.title} on {preferred_date} at {preferred_time}.",
        "success",
    )
    return RedirectResponse(url=f"/properties/{property_id}", status_code=303)


@router.get("/matching")
def matching_page(
    request: Request,
    category: Optional[str] = None,
    property_type: Optional[str] = None,
    bedrooms: Optional[int] = None,
    max_budget: Optional[int] = None,
    min_power_hours: Optional[int] = None,
    negotiable_only: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    """Personalised Property Matching & Inspection Coordination."""
    all_props = list(
        session.exec(select(Property).where(Property.status == "Available")).all()
    )

    scored_matches = []
    for p in all_props:
        score = 72
        reasons = ["Verified Authority Shield"]

        if category and category != "Any":
            if p.category.lower() == category.lower():
                score += 10
                reasons.append(f"Matches {p.category} preference")
            else:
                score -= 20

        if property_type and property_type != "Any":
            if p.property_type.lower() == property_type.lower():
                score += 12
                reasons.append(f"Exact {p.property_type} architecture")
            else:
                score -= 15

        if bedrooms is not None and bedrooms > 0 and p.property_type != "Land":
            if p.bedrooms == bedrooms:
                score += 8
                reasons.append(f"{p.bedrooms} Bedrooms match")
            elif p.bedrooms >= bedrooms:
                score += 4

        if max_budget and max_budget > 0:
            if p.total_initial_commitment <= max_budget:
                score += 10
                reasons.append("Full commitment within budget")
            elif p.base_price <= max_budget:
                score += 5
            else:
                score -= 18

        if min_power_hours and p.power_hours_per_day >= min_power_hours:
            score += 6
            reasons.append(f"{p.power_hours_per_day}hrs/day verified power")

        if negotiable_only:
            if p.is_negotiable:
                score += 5
                reasons.append("Open to Deal Room negotiation")
            else:
                score -= 12

        bounded_score = max(45, min(99, score))
        scored_matches.append(
            {
                "property": p,
                "match_score": bounded_score,
                "match_reasons": reasons[:3],
            }
        )

    scored_matches.sort(key=lambda item: item["match_score"], reverse=True)

    return render_page(
        request,
        "properties/matching.html",
        {
            "matches": scored_matches,
            "prefs": {
                "category": category or "Any",
                "property_type": property_type or "Any",
                "bedrooms": bedrooms if bedrooms is not None else 3,
                "max_budget": max_budget or 15000000,
                "min_power_hours": min_power_hours or 20,
                "negotiable_only": negotiable_only,
            },
        },
    )


@router.post("/properties/create")
def create_property(
    request: Request,
    title: str = Form(...),
    category: str = Form("Rent"),
    property_type: str = Form("Duplex"),
    location: str = Form("Maitama District, Abuja"),
    neighbourhood_key: str = Form("maitama-abuja"),
    address_hint: str = Form(...),
    bedrooms: int = Form(0),
    bathrooms: int = Form(0),
    size_sqm: int = Form(320),
    image_file: Optional[UploadFile] = File(None),
    description: str = Form(...),
    features_csv: str = Form("22hrs Power,Treated Water,Biometric Security,Prepaid Meter"),
    authority_role: str = Form("Direct Landlord"),
    authority_document: str = Form("FCDA C of O & AGIS Verification"),
    base_price: int = Form(...),
    legal_fee: int = Form(350000),
    caution_deposit: int = Form(300000),
    service_charge: int = Form(400000),
    c_of_o_fee: int = Form(0),
    r_of_o_fee: int = Form(0),
    tdp_fee: int = Form(0),
    is_negotiable: bool = Form(False),
    min_acceptable_price: int = Form(0),
    power_hours_per_day: int = Form(22),
    session: Session = Depends(get_session),
):
    user = get_current_user(request)
    effective_min = min_acceptable_price if min_acceptable_price > 0 else int(base_price * 0.92)
    nb_info = NEIGHBOURHOODS.get(neighbourhood_key, NEIGHBOURHOODS["maitama-abuja"])

    # Handle uploaded image file from Landlord
    saved_image_url = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85"
    if image_file and image_file.filename:
        ext = Path(image_file.filename).suffix.lower() or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            ext = ".jpg"
        safe_filename = f"prop-{int(datetime.now().timestamp())}{ext}"
        dest_path = UPLOAD_DIR / safe_filename
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        saved_image_url = f"/static/uploads/{safe_filename}"

    # Enforce 7% Agency Fee for Houses/Apartments and 5% for Land Sales
    is_land = property_type == "Land"
    computed_agency_fee = int(base_price * 0.05) if is_land else int(base_price * 0.07)

    # Default C of O, R of O, and TDP fees for Land if landlord left them as 0
    final_c_of_o = (c_of_o_fee if c_of_o_fee > 0 else 1500000) if is_land else 0
    final_r_of_o = (r_of_o_fee if r_of_o_fee > 0 else 750000) if is_land else 0
    final_tdp = (tdp_fee if tdp_fee > 0 else 500000) if is_land else 0

    new_prop = Property(
        title=title.strip(),
        slug=slugify(title),
        category="Buy" if is_land else category,
        property_type=property_type,
        location=location.strip(),
        neighbourhood_key=neighbourhood_key,
        address_hint=address_hint.strip(),
        bedrooms=0 if is_land else bedrooms,
        bathrooms=0 if is_land else bathrooms,
        size_sqm=size_sqm,
        image_url=saved_image_url,
        secondary_image_url=saved_image_url,
        description=description.strip(),
        features_csv=features_csv,
        is_verified=True,
        verification_code=f"EST-VER-{int(datetime.now().timestamp()) % 9000 + 1000}",
        authority_role=authority_role,
        authority_document=authority_document,
        inspected_by_estate=True,
        landlord_name=user["name"],
        landlord_email=user["email"],
        landlord_reputation=user.get("reputation_score", 4.9),
        base_price=base_price,
        price_period="outright" if (is_land or category == "Buy") else "year",
        agency_fee=computed_agency_fee,
        legal_fee=legal_fee,
        caution_deposit=0 if is_land else caution_deposit,
        service_charge=0 if is_land else service_charge,
        survey_or_deed_fee=0,
        c_of_o_fee=final_c_of_o,
        r_of_o_fee=final_r_of_o,
        tdp_fee=final_tdp,
        status="Available",
        last_confirmed_at=datetime.now(timezone.utc),
        power_hours_per_day=power_hours_per_day,
        water_status=nb_info["water_note"],
        drainage_score=9.5,
        road_status=nb_info["roads_note"],
        security_score=9.6,
        is_negotiable=is_negotiable,
        min_acceptable_price=effective_min,
    )
    session.add(new_prop)
    session.commit()
    session.refresh(new_prop)

    set_flash_message(
        request,
        f"Listing '{new_prop.title}' published with Verification Code {new_prop.verification_code}!",
        "success",
    )
    return RedirectResponse(url="/dashboard/landlord", status_code=303)


@router.post("/properties/{property_id}/reconfirm")
def reconfirm_property_availability(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    """Landlord reconfirms availability for the next 7 days."""
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    prop.last_confirmed_at = datetime.now(timezone.utc)
    prop.status = "Available"
    session.add(prop)
    session.commit()

    set_flash_message(
        request,
        f"7-Day availability timer reset for '{prop.title}'. Marked Available for the next 7 days.",
        "success",
    )
    referer = request.headers.get("referer", "/dashboard/landlord")
    return RedirectResponse(url=referer, status_code=303)


@router.post("/properties/{property_id}/toggle-status")
def toggle_property_status(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    """Toggle between Available and Unavailable (Rented/Sold)."""
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    prop.status = "Unavailable" if prop.status == "Available" else "Available"
    if prop.status == "Available":
        prop.last_confirmed_at = datetime.now(timezone.utc)
    session.add(prop)
    session.commit()

    set_flash_message(
        request,
        f"Status for '{prop.title}' updated to '{prop.status}'.",
        "info",
    )
    referer = request.headers.get("referer", "/dashboard/landlord")
    return RedirectResponse(url=referer, status_code=303)


@router.post("/properties/{property_id}/toggle-verify")
def toggle_property_verification(
    request: Request,
    property_id: int,
    session: Session = Depends(get_session),
):
    """Admin verifies or revokes advertiser authority."""
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    prop.is_verified = not prop.is_verified
    session.add(prop)
    session.commit()

    state_label = "Verified & Approved" if prop.is_verified else "Unverified / Flagged for Audit"
    set_flash_message(
        request,
        f"Listing '{prop.title}' is now {state_label}.",
        "success" if prop.is_verified else "warning",
    )
    referer = request.headers.get("referer", "/dashboard/admin")
    return RedirectResponse(url=referer, status_code=303)
