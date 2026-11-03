from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from app.demo_state import USERS_DB, set_flash_message
from app.template_utils import render_page

router = APIRouter(tags=["auth"])


@router.get("/auth")
def auth_redirect(request: Request, mode: str = "login"):
    if mode == "register":
        return RedirectResponse(url="/auth/register", status_code=303)
    return RedirectResponse(url="/auth/login", status_code=303)


@router.get("/auth/login")
def login_page(request: Request):
    return render_page(request, "auth_login.html")


@router.get("/auth/register")
def register_page(request: Request):
    return render_page(request, "auth_register.html")


@router.post("/auth/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form("password123"),
):
    for user in USERS_DB:
        if user["email"].lower() == email.strip().lower():
            request.session["user_email"] = user["email"]
            set_flash_message(
                request,
                f"Signed in as {user['name']} ({user['role'].capitalize()} Dashboard ready).",
                "success",
            )
            return RedirectResponse(url=f"/dashboard/{user['role']}", status_code=303)

    new_user = {
        "id": len(USERS_DB) + 1,
        "name": email.split("@")[0].replace(".", " ").title(),
        "email": email.strip(),
        "password": password,
        "role": "tenant",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        "badge": "Verified Tenant • 5.0★",
        "reputation_score": 5.0,
        "verified_identity": "NIN Verified",
        "phone": "+234 800 000 0000",
    }
    USERS_DB.append(new_user)
    request.session["user_email"] = new_user["email"]
    set_flash_message(request, f"Welcome back, {new_user['name']}!", "success")
    return RedirectResponse(url="/dashboard/tenant", status_code=303)


@router.post("/auth/register")
def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form("+234 803 000 0000"),
    role: str = Form("tenant"),  # "tenant" or "landlord"
    password: str = Form("password123"),
):
    clean_role = role.lower() if role.lower() in ("tenant", "landlord") else "tenant"
    badge = (
        "Verified Property Owner • 5.0★"
        if clean_role == "landlord"
        else "Verified Tenant • 5.0★"
    )
    identity = (
        "Land Registry & NIN Verified"
        if clean_role == "landlord"
        else "NIN & BVN Verified"
    )
    avatar = (
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
        if clean_role == "landlord"
        else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
    )

    new_user = {
        "id": len(USERS_DB) + 1,
        "name": name.strip(),
        "email": email.strip(),
        "password": password,
        "role": clean_role,
        "avatar": avatar,
        "badge": badge,
        "reputation_score": 5.0,
        "verified_identity": identity,
        "phone": phone.strip(),
    }
    USERS_DB.append(new_user)
    request.session["user_email"] = new_user["email"]
    set_flash_message(
        request,
        f"Account created! Welcome to Estate, {new_user['name']} ({clean_role.capitalize()}).",
        "success",
    )
    return RedirectResponse(url=f"/dashboard/{clean_role}", status_code=303)


@router.get("/auth/switch/{role}")
def switch_demo_role(request: Request, role: str):
    """Role switcher helper to jump between Tenant, Landlord, and Admin personas."""
    target_role = role.lower()
    for user in USERS_DB:
        if user["role"] == target_role:
            request.session["user_email"] = user["email"]
            set_flash_message(
                request,
                f"Switched active role to {user['name']} ({target_role.upper()}).",
                "info",
            )
            return RedirectResponse(url=f"/dashboard/{target_role}", status_code=303)
    return RedirectResponse(url="/", status_code=303)
