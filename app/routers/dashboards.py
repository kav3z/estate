from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import Property
from app.demo_state import (
    ACCOUNTABILITY_COMPLAINTS,
    INSPECTIONS_AND_APPLICATIONS,
    NEGOTIATIONS,
    NEIGHBOURHOODS,
    PLATFORM_REVIEWS,
    TENANT_RENTED_OR_BOUGHT,
    USERS_DB,
    get_current_user,
    set_flash_message,
)
from app.template_utils import render_page

router = APIRouter(prefix="/dashboard", tags=["dashboards"])


@router.get("/tenant")
def tenant_dashboard(request: Request, session: Session = Depends(get_session)):
    """
    Tenant Dashboard:
    - Shows all properties bought or rented from the site
    - Allows tenant to write/update reviews & feedback for each bought/rented property AND for the platform
    - Shows active negotiations, scheduled inspections, and Landlord/Tenant accountability tickets
    """
    all_props = list(session.exec(select(Property)).all())
    return render_page(
        request,
        "dashboards/tenant.html",
        {
            "rented_or_bought": TENANT_RENTED_OR_BOUGHT,
            "negotiations": list(NEGOTIATIONS.values()),
            "inspections": INSPECTIONS_AND_APPLICATIONS,
            "complaints": ACCOUNTABILITY_COMPLAINTS,
            "platform_reviews": PLATFORM_REVIEWS,
            "all_properties": all_props,
        },
    )


@router.post("/tenant/property-review")
def submit_tenant_property_review(
    request: Request,
    transaction_id: str = Form(...),
    rating: int = Form(5),
    review_text: str = Form(...),
):
    """Allows tenant to submit/update feedback & review for a property they bought or rented."""
    user = get_current_user(request)
    updated_title = "Property"
    for item in TENANT_RENTED_OR_BOUGHT:
        if item["transaction_id"] == transaction_id:
            item["my_property_rating"] = max(1, min(5, rating))
            item["my_property_review"] = review_text.strip()
            updated_title = item["property_title"]
            break

    # Also mirror to platform reviews feed so visitors see verified buyer/tenant reviews
    PLATFORM_REVIEWS.insert(
        0,
        {
            "id": len(PLATFORM_REVIEWS) + 1,
            "user_name": user["name"],
            "user_role": "Verified Buyer / Tenant",
            "user_avatar": user["avatar"],
            "rating": max(1, min(5, rating)),
            "impact_tag": f"Verified Checkout ({transaction_id})",
            "property_ref": updated_title,
            "comment": review_text.strip(),
            "date": "Just now",
        },
    )

    set_flash_message(
        request,
        f"Your verified review for '{updated_title}' has been saved to your portfolio & published!",
        "success",
    )
    return RedirectResponse(url="/dashboard/tenant", status_code=303)


@router.get("/landlord")
def landlord_dashboard(request: Request, session: Session = Depends(get_session)):
    """
    10 Dashboard for Landlord:
    - Manage SQLite property listings (Create new listing, 7-day availability reconfirmation, mark Available/Unavailable)
    - Manage enquiries, inspections, applications, and automated tenant selection
    - Respond to structured Deal Room offers & view reputation/accountability records
    """
    properties = list(session.exec(select(Property).order_by(Property.id.desc())).all())
    overdue_count = sum(1 for p in properties if p.is_reconfirmation_overdue or p.days_until_reconfirmation_due <= 2)

    return render_page(
        request,
        "dashboards/landlord.html",
        {
            "properties": properties,
            "overdue_count": overdue_count,
            "inspections": INSPECTIONS_AND_APPLICATIONS,
            "negotiations": list(NEGOTIATIONS.values()),
            "complaints": ACCOUNTABILITY_COMPLAINTS,
            "neighbourhoods": list(NEIGHBOURHOODS.values()),
        },
    )


@router.post("/landlord/application/{insp_id}/status")
def update_application_status(
    request: Request,
    insp_id: str,
    new_status: str = Form("Approved for Selection"),
):
    for item in INSPECTIONS_AND_APPLICATIONS:
        if item["id"] == insp_id:
            item["application_status"] = new_status
            set_flash_message(
                request,
                f"Application {insp_id} ({item['applicant_name']}) updated to '{new_status}'.",
                "success",
            )
            break
    return RedirectResponse(url="/dashboard/landlord", status_code=303)


@router.get("/admin")
def admin_dashboard(request: Request, session: Session = Depends(get_session)):
    """
    Admin Dashboard (for site owners):
    - 01 Verify property listings & confirm advertiser authority (Direct Landlord / Mandated Agent)
    - 03 Monitor 7-day reconfirmation compliance across all listings
    - 05 Mediate & resolve Landlord and Tenant accountability complaints
    - Overview of platform inventory, users, and transactions
    """
    properties = list(session.exec(select(Property).order_by(Property.id.desc())).all())
    verified_count = sum(1 for p in properties if p.is_verified)
    available_count = sum(1 for p in properties if p.status == "Available")

    return render_page(
        request,
        "dashboards/admin.html",
        {
            "properties": properties,
            "verified_count": verified_count,
            "available_count": available_count,
            "complaints": ACCOUNTABILITY_COMPLAINTS,
            "users": USERS_DB,
            "transactions": TENANT_RENTED_OR_BOUGHT,
            "reviews": PLATFORM_REVIEWS,
        },
    )


@router.post("/accountability/file")
def file_accountability_complaint(
    request: Request,
    against_name: str = Form(...),
    against_role: str = Form("Landlord"),
    property_title: str = Form(...),
    category: str = Form("Contract / Fee Compliance"),
    severity: str = Form("Medium"),
    description: str = Form(...),
    redirect_to: str = Form("/dashboard/tenant"),
):
    """05 Landlord and tenant accountability: File a documented complaint."""
    user = get_current_user(request)
    new_cmp = {
        "id": f"CMP-{2050 + len(ACCOUNTABILITY_COMPLAINTS) + 1}",
        "filed_by_name": user["name"],
        "filed_by_role": user["role"].capitalize(),
        "against_name": against_name.strip(),
        "against_role": against_role,
        "property_title": property_title.strip(),
        "category": category.strip(),
        "severity": severity,
        "description": description.strip(),
        "status": "Under Review",
        "resolution_note": "Logged in Estate Accountability Ledger. Admin compliance officer assigned.",
        "reputation_impact": "Escrow & Reputation Watch Active",
        "created_at": "Just now",
    }
    ACCOUNTABILITY_COMPLAINTS.insert(0, new_cmp)
    set_flash_message(
        request,
        f"Accountability case {new_cmp['id']} logged and routed to Admin Compliance.",
        "info",
    )
    return RedirectResponse(url=redirect_to, status_code=303)


@router.post("/admin/complaints/{cmp_id}/resolve")
def resolve_complaint(
    request: Request,
    cmp_id: str,
    resolution_note: str = Form("Verified evidence from both parties; resolved in accordance with Estate Charter."),
    reputation_impact: str = Form("Reputation Verified • Issue Closed"),
):
    for cmp_item in ACCOUNTABILITY_COMPLAINTS:
        if cmp_item["id"] == cmp_id:
            cmp_item["status"] = "Resolved"
            cmp_item["resolution_note"] = resolution_note.strip()
            cmp_item["reputation_impact"] = reputation_impact.strip()
            set_flash_message(request, f"Accountability ticket {cmp_id} marked Resolved.", "success")
            break
    return RedirectResponse(url="/dashboard/admin", status_code=303)

