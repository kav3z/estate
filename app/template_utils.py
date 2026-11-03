from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.demo_state import (
    get_current_user,
    get_cart_ids,
    get_flash_message,
    USERS_DB,
)

templates = Jinja2Templates(directory="app/templates")


def format_naira(value: int | float | None) -> str:
    """Format an integer/float as Nigerian Naira e.g. ₦8,500,000."""
    if value is None:
        return "₦0"
    return f"₦{int(value):,}"


def format_naira_compact(value: int | float | None) -> str:
    """Format large Naira values compactly for badges e.g. ₦8.5M or ₦285M."""
    if value is None:
        return "₦0"
    val = float(value)
    if val >= 1_000_000:
        millions = val / 1_000_000
        if millions.is_integer():
            return f"₦{int(millions)}M"
        return f"₦{millions:.1f}M"
    if val >= 1_000:
        return f"₦{int(val // 1_000)}K"
    return f"₦{int(val)}"


templates.env.filters["naira"] = format_naira
templates.env.filters["naira_compact"] = format_naira_compact


def render_page(request: Request, template_name: str, context: dict[str, Any] | None = None):
    """Render a Jinja2 template with common layout context (active user, cart count, flash message)."""
    path = request.url.path
    is_home_page = path == "/"
    is_dashboard_page = path.startswith("/dashboard")
    is_logged_in = bool(request.session.get("is_logged_in", False)) or is_dashboard_page

    ctx: dict[str, Any] = {
        "request": request,
        "current_user": get_current_user(request),
        "demo_users": USERS_DB,
        "cart_ids": get_cart_ids(request),
        "cart_count": len(get_cart_ids(request)),
        "flash": get_flash_message(request),
        "is_home_page": is_home_page,
        "is_dashboard_page": is_dashboard_page,
        "is_logged_in": is_logged_in,
    }
    if context:
        ctx.update(context)
    return templates.TemplateResponse(request=request, name=template_name, context=ctx)

