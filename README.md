# Estate — Verified Housing & Land Listing Platform

**Estate** is a fullstack house and land discovery, negotiation, and escrow checkout platform built with **FastAPI**, **Jinja2 Templates**, **SQLModel (SQLite)**, **Pydantic**, and **`uv`**.

## Core Features Included
- **01 Verified Property Listings**: Authority confirmation (`Direct Landlord` or `Mandated Agent`), C of O / Governor's Consent verification, and Admin verification shield controls.
- **02 Transparent Rental & Purchase Charges**: Upfront Nigerian Naira (`₦`) breakdown of Base Rent/Price, Agency Fee, Legal/Agreement Fee, Caution Deposit, and Service Charge before booking an inspection or checking out.
- **03 Property Update (7-Day Rule)**: Landlords reconfirm availability every 7 days on their dashboard; properties are marked `Unavailable` immediately upon checkout or via landlord toggle.
- **04 Neighbourhood Intelligence**: Telemetry for Electricity (daily hours), Water, Drainage, Roads, and Security + a Verified Resident Feedback portal.
- **05 Landlord & Tenant Accountability**: Documented reputation scores and an interactive Complaint & Dispute Resolution Ledger.
- **06 Platform & Property Reviews**: Dedicated `/reviews` page plus the ability for tenants to review every property they have bought or rented directly from their Tenant Dashboard.
- **07 Help Center (FAQ & Contact Us)**: Interactive FAQ accordion and direct support ticket system at `/help`.
- **08 Transaction-Support Service (Deal Room)**: Structured Offer & Counter-Offer Timeline with live price slider, mandate floor matching, and instant checkout lock for negotiable properties.
- **09 Personalised Property Matching & Inspection Coordination**: Compatibility matcher by house/land type, bedrooms, budget cap, and daily power hours at `/matching`.
- **10 Three Role Dashboards + Multi-Property Escrow Checkout**:
  - **Tenant Dashboard** (`/dashboard/tenant`)
  - **Landlord Dashboard** (`/dashboard/landlord`)
  - **Admin Dashboard** (`/dashboard/admin`)
  - **Multi-Property Selection Tray & Custom Escrow Payment Gateway** (`/transactions/cart` & `/transactions/checkout`)

## Quickstart with `uv`

```bash
# 1. Sync dependencies
uv sync

# 2. Start the FastAPI server
uv run uvicorn app.main:app --reload --port 8000
```

Then open **http://127.0.0.1:8000** in your browser.

