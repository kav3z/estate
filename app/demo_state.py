"""
In-memory Demo & Session State for Estate MVP.
While Property Listings are stored dynamically in SQLite (estate.db),
this module provides pre-populated, interactive state for:
- Users (Tenant, Landlord, Admin) + Signup/Login & instant Role Switcher
- 04 Neighbourhood Intelligence Profiles & Verified Resident Feedback
- 05 Landlord & Tenant Accountability (Reputation profiles & Complaint resolution tickets)
- 06 Platform Reviews & Purchased/Rented Property Reviews
- 07 Help Center (FAQs & Contact Support submissions)
- 08 Transaction-Support Deal Room (Structured Offer & Counter-Offer Timelines)
- 09 & 10 Inspection Bookings, Tenant Applications, and Multi-Property Checkout Cart
"""

from datetime import datetime
from typing import Any
from fastapi import Request

# ---------------------------------------------------------------------------
# 1. DEMO USERS (Tenant, Landlord, Admin)
# ---------------------------------------------------------------------------
USERS_DB: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "Chidi Nwosu",
        "email": "tenant@estate.ng",
        "password": "password123",
        "role": "tenant",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        "badge": "Verified Tenant • 4.95★",
        "reputation_score": 4.95,
        "verified_identity": "NIN & BVN Verified",
        "phone": "+234 803 441 9021",
    },
    {
        "id": 2,
        "name": "Engr. Tunde Bakare",
        "email": "landlord@estate.ng",
        "password": "password123",
        "role": "landlord",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
        "badge": "Verified Property Owner • 4.9★",
        "reputation_score": 4.90,
        "verified_identity": "Land Registry & CAC Verified",
        "phone": "+234 809 210 7780",
    },
    {
        "id": 3,
        "name": "Amara Obi (Estate Admin)",
        "email": "admin@estate.ng",
        "password": "password123",
        "role": "admin",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
        "badge": "Trust & Compliance Officer",
        "reputation_score": 5.00,
        "verified_identity": "Internal Staff Level 4",
        "phone": "+234 700 ESTATE NG",
    },
]

# ---------------------------------------------------------------------------
# 2. NEIGHBOURHOOD INTELLIGENCE PROFILES & VERIFIED RESIDENT FEEDBACK (04)
# ---------------------------------------------------------------------------
NEIGHBOURHOODS: dict[str, dict[str, Any]] = {
    "lekki-phase-1": {
        "key": "lekki-phase-1",
        "name": "Lekki Phase 1, Lagos",
        "tagline": "Premier Waterfront & Commercial-Residential Hub",
        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 22,
        "electricity_note": "EKEDC Band-A Feeder + Central Estate IPP Backup",
        "water_rating": "9.4/10",
        "water_note": "Central Reverse-Osmosis Treatment Plant",
        "drainage_rating": "9.2/10",
        "drainage_note": "Elevated Admiralty Axis — Deep Covered Storm Channels",
        "roads_rating": "9.5/10",
        "roads_note": "Interlocked Inner Closes with Solar Streetlighting",
        "security_rating": "9.7/10",
        "security_note": "Biometric Gate Pass, ANPR Cameras & 24/7 Armed Patrol",
        "avg_rent_2bed": 5500000,
        "avg_rent_4bed": 8500000,
    },
    "old-ikoyi": {
        "key": "old-ikoyi",
        "name": "Old Ikoyi, Lagos",
        "tagline": "Ultra-Prime Diplomatic & Luxury Residential Enclave",
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 24,
        "electricity_note": "Dedicated 33kV Feeder + Dual Redundant Turbines",
        "water_rating": "9.8/10",
        "water_note": "Potable Municipal Trunk + UV Filtration",
        "drainage_rating": "9.8/10",
        "drainage_note": "Zero Flood History — Engineered Canal Outfall",
        "roads_rating": "9.9/10",
        "roads_note": "Dual-Carriageway Tree-Lined Boulevards",
        "security_rating": "9.9/10",
        "security_note": "Diplomatic Zone Surveillance & Rapid Response Squad",
        "avg_rent_2bed": 14000000,
        "avg_rent_4bed": 25000000,
    },
    "ikeja-gra": {
        "key": "ikeja-gra",
        "name": "Ikeja GRA, Lagos",
        "tagline": "Quiet Tree-Lined Heritage Estates Near Airport",
        "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 21,
        "electricity_note": "Ikeja Electric Bilateral Line (21–23 hrs daily)",
        "water_rating": "9.5/10",
        "water_note": "Low-Iron Freshwater Table + Estate Boreholes",
        "drainage_rating": "9.5/10",
        "drainage_note": "Natural Upland Topography — Never Floods",
        "roads_rating": "9.6/10",
        "roads_note": "Newly Resurfaced Asphalt & Dedicated Walkways",
        "security_rating": "9.6/10",
        "security_note": "Controlled Resident Stickers & Close Gates",
        "avg_rent_2bed": 4500000,
        "avg_rent_4bed": 7500000,
    },
    "victoria-island": {
        "key": "victoria-island",
        "name": "Victoria Island Annex, Lagos",
        "tagline": "Walk-to-Work Financial District & Serviced Enclaves",
        "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 22,
        "electricity_note": "VI Independent Power Network + Band-A Grid",
        "water_rating": "9.3/10",
        "water_note": "Desalination & Industrial Treatment Plant",
        "drainage_rating": "9.3/10",
        "drainage_note": "Upgraded Collector Drains along Oniru Corridor",
        "roads_rating": "9.4/10",
        "roads_note": "Paved Estate Boulevards with Fiber Ducts",
        "security_rating": "9.6/10",
        "security_note": "24/7 Corporate & Estate Joint Security Taskforce",
        "avg_rent_2bed": 7000000,
        "avg_rent_4bed": 12000000,
    },
    "yaba-mainland": {
        "key": "yaba-mainland",
        "name": "Yaba Tech Corridor, Lagos",
        "tagline": "Central Mainland Innovation & University Hub",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 18,
        "electricity_note": "Band-A Alagomeji Feeder (18–20 hrs daily)",
        "water_rating": "8.9/10",
        "water_note": "Clean Freshwater Boreholes",
        "drainage_rating": "8.7/10",
        "drainage_note": "Covered Concrete Slab Drains",
        "roads_rating": "9.0/10",
        "roads_note": "Tarred Grid Streets with Quick 3rd Mainland Access",
        "security_rating": "9.1/10",
        "security_note": "Gated Street Associations & Night Vigils",
        "avg_rent_2bed": 3200000,
        "avg_rent_4bed": 5000000,
    },
    "maitama-abuja": {
        "key": "maitama-abuja",
        "name": "Maitama District, Abuja",
        "tagline": "Serene Hills, Wide Boulevards & Diplomatic Residences",
        "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 23,
        "electricity_note": "AEDC Priority Grid + Solar Hybrid Estates",
        "water_rating": "9.7/10",
        "water_note": "Lower Usuma Dam Mains + Filtration",
        "drainage_rating": "9.7/10",
        "drainage_note": "Master-Planned Underground Storm Infrastructure",
        "roads_rating": "9.9/10",
        "roads_note": "Multi-Lane Express Asphalt & Cycle Lanes",
        "security_rating": "9.8/10",
        "security_note": "High-Security Diplomatic Patrol Zone",
        "avg_rent_2bed": 6500000,
        "avg_rent_4bed": 11000000,
    },
    "epe-corridor": {
        "key": "epe-corridor",
        "name": "Epe Growth Corridor, Lagos",
        "tagline": "Fastest Appreciating Land & Eco-Residential Belt",
        "image": "https://images.unsplash.com/photo-1500076656116-558758c991c1?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 16,
        "electricity_note": "Expanding Grid + Solar Mini-Grid Ready",
        "water_rating": "9.6/10",
        "water_note": "100% Pure Natural Freshwater Table",
        "drainage_rating": "9.0/10",
        "drainage_note": "High Elevation Dry Laterite Soil",
        "roads_rating": "9.2/10",
        "roads_note": "Newly Constructed 6-Lane Rigid Concrete Highway",
        "security_rating": "9.0/10",
        "security_note": "Perimeter-Fenced Gatehouse Communities",
        "avg_rent_2bed": 1500000,
        "avg_rent_4bed": 2800000,
    },
}

RESIDENT_FEEDBACK: list[dict[str, Any]] = [
    {
        "id": 1,
        "neighbourhood_key": "lekki-phase-1",
        "resident_name": "Kemi Adeyemi",
        "residency_duration": "3 Years Verified Resident",
        "verification_badge": "Utility Bill & Tenancy Verified",
        "rating": 5,
        "power_report": "22 hrs/day average",
        "water_report": "Odorless & clear treated water",
        "drainage_report": "Zero waterlogging even during July peak rain",
        "comment": (
            "Living off Admiralty Way has been effortless. The estate central plant switches over in 15 seconds, "
            "and street security requires a dynamic code from residents before any visitor enters."
        ),
        "created_at": "2 days ago",
    },
    {
        "id": 2,
        "neighbourhood_key": "ikeja-gra",
        "resident_name": "Dr. Olumide Bamidele",
        "residency_duration": "5 Years Verified Homeowner",
        "verification_badge": "Land Use Charge Verified",
        "rating": 5,
        "power_report": "21 hrs/day Bilateral Feeder",
        "water_report": "Freshwater borehole, zero iron staining",
        "drainage_report": "Naturally elevated terrain, completely dry",
        "comment": (
            "If you value quiet evenings, mature trees, and genuine Band-A electricity without noisy generators, "
            "Oduduwa Crescent in Ikeja GRA is unmatched in Lagos."
        ),
        "created_at": "5 days ago",
    },
    {
        "id": 3,
        "neighbourhood_key": "yaba-mainland",
        "resident_name": "Tosin Falana",
        "residency_duration": "2 Years Verified Resident",
        "verification_badge": "Tenancy Contract Verified",
        "rating": 4,
        "power_report": "18 hrs/day PHCN",
        "water_report": "Clean borehole water",
        "drainage_report": "Drains cleared quarterly by street association",
        "comment": (
            "Commuting to Victoria Island takes 18 minutes via Third Mainland Bridge. Fiber internet speeds "
            "are fantastic and the neighbourhood is super walkable."
        ),
        "created_at": "1 week ago",
    },
    {
        "id": 4,
        "neighbourhood_key": "old-ikoyi",
        "resident_name": "Ngozi Kachikwu",
        "residency_duration": "4 Years Verified Resident",
        "verification_badge": "Deed & Utility Verified",
        "rating": 5,
        "power_report": "24 hrs/day uninterrupted",
        "water_report": "Hospital-grade filtered water",
        "drainage_report": "10/10 engineered drainage",
        "comment": (
            "Complete peace of mind. Morning jogs along Bourdillon feel safe at 5:30 AM and power has not blinked once this quarter."
        ),
        "created_at": "2 weeks ago",
    },
]

# ---------------------------------------------------------------------------
# 3. TENANT'S PURCHASED / RENTED PROPERTIES & REVIEWS (Extra Note + 06)
# ---------------------------------------------------------------------------
TENANT_RENTED_OR_BOUGHT: list[dict[str, Any]] = [
    {
        "transaction_id": "EST-TX-99410",
        "property_id": 8,
        "property_title": "Veranda Court Serviced 3-Bed Terrace",
        "property_location": "Chevron Drive, Lekki, Lagos",
        "property_image": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=800&q=80",
        "category": "Rent",
        "landlord_name": "Engr. Tunde Bakare",
        "amount_paid": 7800000,
        "date_completed": "14 Oct 2026",
        "payment_method": "Estate Escrow Bank Transfer",
        "my_property_rating": 5,
        "my_property_review": (
            "Exact cost breakdown matched my checkout receipt to the last Naira. The landlord handed over keys "
            "within 24 hours and the property was immediately marked Unavailable on Estate."
        ),
    },
    {
        "transaction_id": "EST-TX-88204",
        "property_id": 4,
        "property_title": "Terra Crest Serviced Land Plot (600 SQM)",
        "property_location": "Victoria Island Annex, Lagos",
        "property_image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
        "category": "Buy",
        "landlord_name": "Engr. Tunde Bakare",
        "amount_paid": 94400000,
        "date_completed": "02 Sep 2026",
        "payment_method": "Estate Escrow Tranche",
        "my_property_rating": 5,
        "my_property_review": (
            "Negotiated ₦5,000,000 off the asking price using Estate's structured Deal Room. Survey and C of O "
            "were already verified so allocation took less than 48 hours."
        ),
    },
]

PLATFORM_REVIEWS: list[dict[str, Any]] = [
    {
        "id": 1,
        "user_name": "Chidi Nwosu",
        "user_role": "Verified Tenant & Land Buyer",
        "user_avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "Saved ₦700k in Negotiated Rent & Avoided Fake Agents",
        "property_ref": "Veranda Court Serviced 3-Bed Terrace",
        "comment": (
            "Before Estate, I wasted ₦60,000 on inspection fees for houses that were already rented out! "
            "Estate's 7-day availability reconfirmation and upfront charge calculator showed me the exact agency, "
            "legal, and caution deposit before I even booked a viewing."
        ),
        "date": "3 days ago",
    },
    {
        "id": 2,
        "user_name": "Zainab Lawal",
        "user_role": "Verified Tenant (Ikeja GRA)",
        "user_avatar": "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "Neighbourhood Power & Drainage Stats Were 100% Accurate",
        "property_ref": "Lakeside Tranquility Nordic Bungalow",
        "comment": (
            "Agents always claim '24 hours light' until you move in. Estate's Neighbourhood Intelligence showed "
            "21 hrs/day verified by actual residents on Oduduwa Crescent, and it has been spot on since I moved in."
        ),
        "date": "1 week ago",
    },
    {
        "id": 3,
        "user_name": "Engr. Tunde Bakare",
        "user_role": "Verified Landlord (6 Properties)",
        "user_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "Zero Unqualified Calls — Structured Offer Timeline",
        "property_ref": "Serenity Pines Contemporary Duplex",
        "comment": (
            "The Landlord Dashboard lets me screen verified tenants, review structured price offers without endless "
            "WhatsApp back-and-forth, and reconfirm availability in one click every 7 days."
        ),
        "date": "2 weeks ago",
    },
]

# ---------------------------------------------------------------------------
# 4. LANDLORD & TENANT ACCOUNTABILITY / COMPLAINT RESOLUTION SYSTEM (05)
# ---------------------------------------------------------------------------
ACCOUNTABILITY_COMPLAINTS: list[dict[str, Any]] = [
    {
        "id": "CMP-2041",
        "filed_by_name": "Chidi Nwosu",
        "filed_by_role": "Tenant",
        "against_name": "Engr. Tunde Bakare",
        "against_role": "Landlord",
        "property_title": "Veranda Court Serviced 3-Bed Terrace",
        "category": "Service Charge Reconciliation",
        "severity": "Medium",
        "description": "Requested itemized diesel consumption receipt for Q3 estate generator service charge.",
        "status": "Resolved",
        "resolution_note": "Landlord uploaded audited estate meter ledger within 18 hours. Both parties signed off.",
        "reputation_impact": "+0.05 Bonus for Fast Resolution",
        "created_at": "18 Oct 2026",
    },
    {
        "id": "CMP-2048",
        "filed_by_name": "Engr. Tunde Bakare",
        "filed_by_role": "Landlord",
        "against_name": "Former Applicant (ID #812)",
        "against_role": "Tenant",
        "property_title": "Serenity Pines Contemporary Duplex",
        "category": "Missed Scheduled Inspection",
        "severity": "Low",
        "description": "Prospective tenant booked 10:00 AM Saturday physical inspection but did not show up or cancel.",
        "status": "Under Review",
        "resolution_note": "Compliance team notified applicant; 1 attendance strike logged on applicant profile.",
        "reputation_impact": "Pending Admin Mediation",
        "created_at": "01 Nov 2026",
    },
    {
        "id": "CMP-2052",
        "filed_by_name": "Adaeze Okafor",
        "filed_by_role": "Tenant",
        "against_name": "Unverified Third-Party Agent",
        "against_role": "Agent",
        "property_title": "Flagged Duplicate Listing (Removed)",
        "category": "Unauthorized Listing Attempt",
        "severity": "High",
        "description": "Reported an external agent attempting to re-upload photos of a verified Direct Landlord listing.",
        "status": "Resolved",
        "resolution_note": "Admin revoked agent access and locked listing under EST-VER-8821 Direct Landlord authority.",
        "reputation_impact": "Fake Ad Blocked Automatically",
        "created_at": "02 Nov 2026",
    },
]

# ---------------------------------------------------------------------------
# 5. TRANSACTION-SUPPORT NEGOTIATIONS ("DEAL ROOM" TIMELINES) (08)
# ---------------------------------------------------------------------------
NEGOTIATIONS: dict[int, dict[str, Any]] = {
    1: {
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex",
        "tenant_name": "Chidi Nwosu",
        "landlord_name": "Engr. Tunde Bakare",
        "listed_price": 8500000,
        "current_agreed_price": 8000000,
        "status": "Counter-Offer Active",  # "Offer Sent", "Counter-Offer Active", "Accepted", "Declined"
        "payment_tenure": "1 Year Annual Lease",
        "move_in_target": "15 Nov 2026",
        "events": [
            {
                "step": "01",
                "actor": "System Verification",
                "role": "system",
                "badge": "Authority Confirmed",
                "proposed_price": 8500000,
                "note": "Listing EST-VER-8821 verified as Negotiable by Direct Landlord (Engr. Tunde Bakare).",
                "timestamp": "Yesterday, 09:15 AM",
            },
            {
                "step": "02",
                "actor": "Chidi Nwosu (Tenant)",
                "role": "tenant",
                "badge": "Initial Structured Offer",
                "proposed_price": 7800000,
                "note": "Ready to pay full commitment within 48 hours via Estate Escrow if we can close at ₦7,800,000/yr.",
                "timestamp": "Yesterday, 02:30 PM",
            },
            {
                "step": "03",
                "actor": "Engr. Tunde Bakare (Landlord)",
                "role": "landlord",
                "badge": "Landlord Counter-Offer",
                "proposed_price": 8000000,
                "note": "Appreciate your verified profile! I can approve ₦8,000,000/yr inclusive of exterior repainting before move-in.",
                "timestamp": "Today, 10:05 AM",
            },
        ],
    },
    4: {
        "property_id": 4,
        "property_title": "Terra Crest Serviced Land Plot (600 SQM)",
        "tenant_name": "Chidi Nwosu",
        "landlord_name": "Engr. Tunde Bakare",
        "listed_price": 95000000,
        "current_agreed_price": 90000000,
        "status": "Accepted",
        "payment_tenure": "Outright Purchase (Escrow Protected)",
        "move_in_target": "Immediate Allocation",
        "events": [
            {
                "step": "01",
                "actor": "Chidi Nwosu (Tenant/Buyer)",
                "role": "tenant",
                "badge": "Purchase Offer",
                "proposed_price": 90000000,
                "note": "Offering ₦90,000,000 single-tranche settlement upon verification of Registered Survey #LA/2025/882.",
                "timestamp": "3 days ago",
            },
            {
                "step": "02",
                "actor": "Engr. Tunde Bakare (Landlord)",
                "role": "landlord",
                "badge": "Offer Accepted ✓",
                "proposed_price": 90000000,
                "note": "Offer accepted. Price locked at ₦90,000,000 for your checkout.",
                "timestamp": "2 days ago",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# 6. INSPECTIONS & TENANT APPLICATIONS (09 & 10)
# ---------------------------------------------------------------------------
INSPECTIONS_AND_APPLICATIONS: list[dict[str, Any]] = [
    {
        "id": "INSP-501",
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex",
        "location": "Lekki Phase 1, Lagos",
        "applicant_name": "Chidi Nwosu",
        "applicant_score": "4.95★ Verified Tenant",
        "preferred_date": "Saturday, 07 Nov 2026",
        "preferred_time": "11:00 AM",
        "inspection_type": "Physical On-Site Viewing",
        "application_status": "Approved for Selection",  # "Pending Review", "Inspection Confirmed", "Approved for Selection"
        "note": "Pre-vetted income & NIN verified. Transparent cost breakdown accepted.",
    },
    {
        "id": "INSP-502",
        "property_id": 3,
        "property_title": "Lakeside Tranquility Nordic Bungalow",
        "location": "Ikeja GRA, Lagos",
        "applicant_name": "Chidi Nwosu",
        "applicant_score": "4.95★ Verified Tenant",
        "preferred_date": "Tuesday, 10 Nov 2026",
        "preferred_time": "02:00 PM",
        "inspection_type": "Live 4K Video + Physical",
        "application_status": "Inspection Confirmed",
        "note": "Matched via Estate Personalised Property Matcher (98% Compatibility).",
    },
    {
        "id": "INSP-503",
        "property_id": 2,
        "property_title": "Prairie Vista Glass Villa",
        "location": "Old Ikoyi, Lagos",
        "applicant_name": "Chief Emeka Onoh",
        "applicant_score": "4.88★ Verified Buyer",
        "preferred_date": "Thursday, 12 Nov 2026",
        "preferred_time": "04:00 PM",
        "inspection_type": "Private Executive Tour",
        "application_status": "Pending Review",
        "note": "Proof of funds uploaded to Estate Escrow vault.",
    },
]

# ---------------------------------------------------------------------------
# 7. HELP CENTER: FAQs & SUPPORT TICKETS (07)
# ---------------------------------------------------------------------------
FAQS: list[dict[str, str]] = [
    {
        "category": "Verification & Anti-Fraud",
        "question": "How does Estate verify that a property is genuine and the advertiser has authority?",
        "answer": (
            "Every property displaying the 'Verified by Estate' shield goes through a 3-step check: "
            "(1) Title & ownership document verification (C of O, Governor's Consent, or Registered Deed), "
            "(2) Signed Mandate or Direct Landlord identity match (NIN/CAC), and "
            "(3) On-site physical inspection with geo-tagged media."
        ),
    },
    {
        "category": "Transparent Charges",
        "question": "Are there any hidden inspection, agency, or legal fees after I commit?",
        "answer": (
            "Never. Our Transparent Rental & Purchase Calculator breaks down Base Rent/Price, Agency Fee, "
            "Legal/Agreement Fee, Caution Deposit, and Service Charge upfront on every property page before you "
            "book an inspection or add to cart."
        ),
    },
    {
        "category": "7-Day Availability Rule",
        "question": "How do you stop agents from advertising houses that have already been rented out?",
        "answer": (
            "Landlords must reconfirm availability on their dashboard every 7 days. If a listing is not reconfirmed "
            "within 7 days, it is flagged as overdue, and the moment a tenant completes checkout, the property is "
            "automatically marked 'Unavailable'."
        ),
    },
    {
        "category": "Neighbourhood Intelligence",
        "question": "Who provides the electricity, water, drainage, and security ratings?",
        "answer": (
            "Metrics combine Estate's field telemetry (feeder band classification & elevation data) with reviews "
            "from Verified Residents who have uploaded proof of residency (utility bill or active tenancy agreement)."
        ),
    },
    {
        "category": "Negotiation & Escrow Checkout",
        "question": "How does the Negotiation Deal Room work?",
        "answer": (
            "When a landlord marks a listing as 'Negotiable', you can propose a structured offer amount and payment "
            "tenure in the Deal Room. Once the landlord accepts your offer or you accept their counter-offer, "
            "your checkout price updates automatically."
        ),
    },
]

SUPPORT_TICKETS: list[dict[str, Any]] = [
    {
        "ticket_id": "HLP-901",
        "name": "Chidi Nwosu",
        "email": "tenant@estate.ng",
        "topic": "Escrow Payment Receipt Verification",
        "message": "Can I download a stamped PDF receipt for my company housing allowance reimbursement?",
        "status": "Answered — Available on Checkout Receipt page",
        "created_at": "Yesterday",
    }
]


# ---------------------------------------------------------------------------
# SESSION HELPERS
# ---------------------------------------------------------------------------
def get_current_user(request: Request) -> dict[str, Any]:
    """Return the active user from session, defaulting to the Demo Tenant so the site works out-of-the-box."""
    user_email = request.session.get("user_email", "tenant@estate.ng")
    for user in USERS_DB:
        if user["email"].lower() == user_email.lower():
            return user
    return USERS_DB[0]


def get_cart_ids(request: Request) -> list[int]:
    """Return list of property IDs currently selected in the tenant's checkout tray."""
    if "cart_ids" not in request.session:
        # Pre-populate with Property #1 so user can immediately test checkout or add/remove more
        request.session["cart_ids"] = [1]
    return request.session["cart_ids"]


def get_effective_base_price(property_obj: Any) -> int:
    """Return negotiated price if an offer is Accepted or Active in the Deal Room, else listed base_price."""
    neg = NEGOTIATIONS.get(property_obj.id)
    if neg and neg.get("status") == "Accepted":
        return int(neg["current_agreed_price"])
    return int(property_obj.base_price)


def get_flash_message(request: Request) -> dict[str, str] | None:
    """Pop and return one-time flash notification from session."""
    return request.session.pop("flash", None)


def set_flash_message(request: Request, title: str, kind: str = "success") -> None:
    request.session["flash"] = {"title": title, "kind": kind}

