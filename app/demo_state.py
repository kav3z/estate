"""
In-memory Demo & Session State for Estate MVP.
While Property Listings are stored dynamically in SQLite (estate.db),
this module provides pre-populated, interactive state for:
- Users (Tenant, Landlord, Admin) + Signup/Login & Role Switcher
- Neighbourhood Intelligence Profiles & Verified Resident Feedback (Abuja majority + Lagos)
- Landlord & Tenant Accountability (Reputation profiles & Complaint resolution tickets)
- Platform Reviews (mix of mostly positive 5★/4★ reviews and realistic critical 2★/1★ reviews)
- Help Center (FAQs & Contact Support submissions)
- Transaction-Support Deal Room (Structured Offer & Counter-Offer Timelines)
- Inspection Bookings, Tenant Applications, and Multi-Property Checkout Cart
"""

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
        "verified_identity": "AGIS Land Registry & CAC Verified",
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
# 2. NEIGHBOURHOOD INTELLIGENCE PROFILES & VERIFIED RESIDENT FEEDBACK
#    (Majority Abuja districts + Lekki Phase 1, Lagos)
# ---------------------------------------------------------------------------
NEIGHBOURHOODS: dict[str, dict[str, Any]] = {
    "maitama-abuja": {
        "key": "maitama-abuja",
        "name": "Maitama District, Abuja",
        "tagline": "Serene Hills, Wide Boulevards & Diplomatic Residences",
        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 23,
        "electricity_note": "AEDC Priority Band-A Grid + Solar Hybrid Estates",
        "water_rating": "9.7/10",
        "water_note": "Lower Usuma Dam Mains + Triple Filtration",
        "drainage_rating": "9.8/10",
        "drainage_note": "Master-Planned Underground Storm Infrastructure",
        "roads_rating": "9.9/10",
        "roads_note": "Multi-Lane Express Asphalt & Solar Streetlights",
        "security_rating": "9.8/10",
        "security_note": "High-Security Diplomatic Patrol Zone & Biometric Gates",
        "avg_rent_2bed": 6500000,
        "avg_rent_4bed": 10000000,
    },
    "asokoro-abuja": {
        "key": "asokoro-abuja",
        "name": "Asokoro District, Abuja",
        "tagline": "Ultra-Prime Presidential & Diplomatic Residential Enclave",
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 24,
        "electricity_note": "Dedicated 33kV Priority Feeder + Estate Backup",
        "water_rating": "9.9/10",
        "water_note": "FCT Municipal Trunk + UV Hospital-Grade Filtration",
        "drainage_rating": "9.9/10",
        "drainage_note": "Elevated Rock Topography — Zero Flood History",
        "roads_rating": "9.9/10",
        "roads_note": "Dual-Carriageway Tree-Lined Diplomatic Boulevards",
        "security_rating": "9.9/10",
        "security_note": "24/7 Diplomatic Zone Surveillance & Rapid Response",
        "avg_rent_2bed": 8500000,
        "avg_rent_4bed": 18000000,
    },
    "wuse-2-abuja": {
        "key": "wuse-2-abuja",
        "name": "Wuse II, Abuja",
        "tagline": "Central Commercial-Residential Hub & Quiet Tree-Lined Closes",
        "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 22,
        "electricity_note": "AEDC Band-A Aminu Kano Feeder (22 hrs daily)",
        "water_rating": "9.5/10",
        "water_note": "Constant FCT Water Board Supply + Estate Boreholes",
        "drainage_rating": "9.5/10",
        "drainage_note": "Deep Covered Storm Collector Channels",
        "roads_rating": "9.7/10",
        "roads_note": "Smooth Asphalt Grid with Dedicated Pedestrian Walkways",
        "security_rating": "9.6/10",
        "security_note": "Gated Residential Closes & 24/7 Smart CCTV",
        "avg_rent_2bed": 4500000,
        "avg_rent_4bed": 8000000,
    },
    "guzape-abuja": {
        "key": "guzape-abuja",
        "name": "Guzape District, Abuja",
        "tagline": "Fast-Rising Luxury Hilltop Views & Serviced Plots",
        "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 22,
        "electricity_note": "Underground High-Tension Feeder + Solar Estates",
        "water_rating": "9.4/10",
        "water_note": "FCT Mains Extension + Deep Rock Boreholes",
        "drainage_rating": "9.7/10",
        "drainage_note": "Natural Hilltop Gradient — Instant Rainwater Runoff",
        "roads_rating": "9.6/10",
        "roads_note": "Newly Constructed FCDA Hilltop Boulevards",
        "security_rating": "9.7/10",
        "security_note": "Controlled Estate Gatehouses & Armed Mobile Patrol",
        "avg_rent_2bed": 5000000,
        "avg_rent_4bed": 9500000,
    },
    "jabi-abuja": {
        "key": "jabi-abuja",
        "name": "Jabi Lake Axis, Abuja",
        "tagline": "Modern Waterfront Lifestyle, Retail & Tech Professional Hub",
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 20,
        "electricity_note": "AEDC Band-A Feeder (20 hrs daily average)",
        "water_rating": "9.3/10",
        "water_note": "FCT Water Board + Central Estate Treatment",
        "drainage_rating": "9.3/10",
        "drainage_note": "Engineered Lake Outfall & Covered Street Drains",
        "roads_rating": "9.5/10",
        "roads_note": "Tarred Grid Streets with Fiber-Optic Conduits",
        "security_rating": "9.4/10",
        "security_note": "Biometric Access & Perimeter Surveillance",
        "avg_rent_2bed": 4000000,
        "avg_rent_4bed": 7000000,
    },
    "katampe-abuja": {
        "key": "katampe-abuja",
        "name": "Katampe Extension, Abuja",
        "tagline": "Elevated Diplomatic Enclave with Central Expressway Access",
        "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 22,
        "electricity_note": "Katampe 132/33kV Substation Direct Feeder",
        "water_rating": "9.5/10",
        "water_note": "FCT Water Board + Borehole Backup",
        "drainage_rating": "9.6/10",
        "drainage_note": "Elevated Terrain with Lined Storm Drains",
        "roads_rating": "9.7/10",
        "roads_note": "Direct Nnamdi Azikiwe Expressway Interchange",
        "security_rating": "9.7/10",
        "security_note": "Diplomatic Enclave Gate Pass & Patrol",
        "avg_rent_2bed": 4500000,
        "avg_rent_4bed": 8500000,
    },
    "lugbe-abuja": {
        "key": "lugbe-abuja",
        "name": "Airport Road / Lugbe, Abuja",
        "tagline": "High-Growth Residential & Serviced Land Corridor",
        "image": "https://images.unsplash.com/photo-1500076656116-558758c991c1?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 19,
        "electricity_note": "Airport Corridor Grid + Solar Mini-Grid Ready",
        "water_rating": "9.2/10",
        "water_note": "Clean Deep-Aquifer Borehole Network",
        "drainage_rating": "9.1/10",
        "drainage_note": "Dry Savannah Table Land",
        "roads_rating": "9.5/10",
        "roads_note": "10-Lane Airport Expressway Access",
        "security_rating": "9.2/10",
        "security_note": "Perimeter-Fenced Gated Estate Communities",
        "avg_rent_2bed": 2200000,
        "avg_rent_4bed": 4000000,
    },
    "lekki-phase-1": {
        "key": "lekki-phase-1",
        "name": "Lekki Phase 1, Lagos",
        "tagline": "Premier Coastal Waterfront & Commercial-Residential Hub",
        "image": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=900&q=80",
        "electricity_hours": 20,
        "electricity_note": "EKEDC Band-A Feeder + Central Estate IPP Backup",
        "water_rating": "9.2/10",
        "water_note": "Central Reverse-Osmosis Treatment Plant",
        "drainage_rating": "9.1/10",
        "drainage_note": "Elevated Admiralty Axis — Covered Storm Channels",
        "roads_rating": "9.4/10",
        "roads_note": "Interlocked Inner Closes with Solar Streetlighting",
        "security_rating": "9.6/10",
        "security_note": "Biometric Gate Pass, ANPR Cameras & 24/7 Patrol",
        "avg_rent_2bed": 5500000,
        "avg_rent_4bed": 8500000,
    },
}

RESIDENT_FEEDBACK: list[dict[str, Any]] = [
    {
        "id": 1,
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex",
        "neighbourhood_key": "maitama-abuja",
        "resident_name": "Chidi Nwosu",
        "residency_duration": "Verified Paid Tenant",
        "verification_badge": "Escrow Payment & Tenancy Verified",
        "rating": 5,
        "power_report": "23 hrs/day AEDC + Hybrid",
        "water_report": "Crystal clear FCT Water Board supply",
        "drainage_report": "Zero waterlogging, underground storm drains",
        "comment": (
            "After paying via Estate Escrow and moving into Maitama, the 23 hrs/day power rating has been 100% accurate. "
            "Water pressure is strong and night security on Gana Street is top-tier."
        ),
        "created_at": "2 days ago",
    },
    {
        "id": 2,
        "property_id": 4,
        "property_title": "Terra Crest Serviced Land Plot (600 SQM)",
        "neighbourhood_key": "guzape-abuja",
        "resident_name": "Chidi Nwosu",
        "residency_duration": "Verified Paid Land Buyer",
        "verification_badge": "Escrow Payment & TDP Verified",
        "rating": 5,
        "power_report": "22 hrs/day underground feeder",
        "water_report": "FCT trunk mains connected at plot boundary",
        "drainage_report": "Elevated Guzape hillside, completely flood-free",
        "comment": (
            "Purchased my 600 SQM plot here on Estate. Receiving the C of O, R of O, and TDP breakdown upfront made due diligence "
            "at AGIS effortless. The hilltop road paving is already completed."
        ),
        "created_at": "5 days ago",
    },
    {
        "id": 3,
        "property_id": 3,
        "property_title": "Lakeside Tranquility Nordic Bungalow",
        "neighbourhood_key": "wuse-2-abuja",
        "resident_name": "Dr. Halima Yusuf",
        "residency_duration": "2 Years Verified Paid Tenant",
        "verification_badge": "Escrow Payment Verified",
        "rating": 5,
        "power_report": "22 hrs/day Band-A Feeder",
        "water_report": "Constant municipal water + borehole backup",
        "drainage_report": "Deep covered channels, dry all year",
        "comment": (
            "Wuse II off Aminu Kano is super central yet surprisingly quiet inside the close. "
            "Everything promised in the Neighbourhood Intelligence report matched reality."
        ),
        "created_at": "1 week ago",
    },
    {
        "id": 4,
        "property_id": 8,
        "property_title": "Veranda Court Serviced 3-Bed Terrace",
        "neighbourhood_key": "lekki-phase-1",
        "resident_name": "Chidi Nwosu",
        "residency_duration": "Verified Paid Tenant",
        "verification_badge": "Escrow Payment Verified",
        "rating": 5,
        "power_report": "20 hrs/day Estate IPP",
        "water_report": "Odorless & clear reverse-osmosis water",
        "drainage_report": "Interlocked road stayed dry during heavy rain",
        "comment": (
            "Checked out this terrace on Estate. The central estate plant switches over in seconds and visitor access is strictly via code."
        ),
        "created_at": "2 weeks ago",
    },
]

# ---------------------------------------------------------------------------
# 3. TENANT'S PURCHASED / RENTED PROPERTIES & REVIEWS
#    (Includes properties #1, #4, and #8 so Demo Tenant can immediately test
#     submitting a Property & Area review directly on those property pages!)
# ---------------------------------------------------------------------------
TENANT_RENTED_OR_BOUGHT: list[dict[str, Any]] = [
    {
        "transaction_id": "EST-TX-99410",
        "property_id": 8,
        "property_title": "Veranda Court Serviced 3-Bed Terrace",
        "property_location": "Lekki Phase 1, Lagos",
        "property_image": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=800&q=80",
        "category": "Rent",
        "landlord_name": "Engr. Tunde Bakare",
        "amount_paid": 7620000,
        "date_completed": "14 Oct 2026",
        "payment_method": "Estate Escrow Bank Transfer",
        "my_property_rating": 5,
        "my_property_review": (
            "Exact 7% agency fee and cost breakdown matched my checkout receipt to the last Naira. The landlord handed over keys "
            "within 24 hours and the property was immediately marked Unavailable on Estate."
        ),
    },
    {
        "transaction_id": "EST-TX-88204",
        "property_id": 4,
        "property_title": "Terra Crest Serviced Land Plot (600 SQM)",
        "property_location": "Guzape District, Abuja",
        "property_image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
        "category": "Buy",
        "landlord_name": "Engr. Tunde Bakare",
        "amount_paid": 90100000,
        "date_completed": "02 Sep 2026",
        "payment_method": "Estate Escrow Tranche",
        "my_property_rating": 5,
        "my_property_review": (
            "Negotiated ₦5,000,000 off the asking price in the Deal Room. Having C of O, R of O, and TDP clearly itemized "
            "alongside the 5% land agency fee made allocation in Guzape seamless."
        ),
    },
    {
        "transaction_id": "EST-TX-77109",
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex",
        "property_location": "Maitama District, Abuja",
        "property_image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
        "category": "Rent",
        "landlord_name": "Engr. Tunde Bakare",
        "amount_paid": 12350000,
        "date_completed": "01 Nov 2026",
        "payment_method": "Estate Escrow Card (Visa/Verve)",
        "my_property_rating": 5,
        "my_property_review": (
            "Secured a second unit in Maitama through Estate. Power and water in the neighbourhood are exactly as stated."
        ),
    },
]

# ---------------------------------------------------------------------------
# 4. PLATFORM REVIEWS (Majority Positive 5★/4★ + Some Critical/Bad 2★ Reviews)
# ---------------------------------------------------------------------------
PLATFORM_REVIEWS: list[dict[str, Any]] = [
    {
        "id": 1,
        "user_name": "Chidi Nwosu",
        "user_role": "Verified Tenant & Land Buyer (Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "7% House Agency Cap & Zero Fake Agents",
        "property_ref": "Serenity Pines Contemporary Duplex (Maitama)",
        "comment": (
            "Before Estate, Abuja agents demanded 10%–15% agency fees and wasted my time on houses that were already rented! "
            "Estate's capped 7% house agency fee and 7-day availability reconfirmation showed me the exact commitment upfront."
        ),
        "date": "2 days ago",
    },
    {
        "id": 2,
        "user_name": "Zainab Lawal",
        "user_role": "Verified Tenant (Wuse II, Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "Neighbourhood Power & Water Stats Were 100% Accurate",
        "property_ref": "Lakeside Tranquility Nordic Bungalow",
        "comment": (
            "Only verified paid tenants can post area reviews on property pages, which means zero fake hype. "
            "The 22 hrs/day AEDC power report in Wuse II has been completely accurate since I moved in."
        ),
        "date": "5 days ago",
    },
    {
        "id": 3,
        "user_name": "Damilola Ojo",
        "user_role": "Prospective Tenant (Jabi, Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
        "rating": 2,
        "impact_tag": "Strict Non-Negotiable Filter on Some Bungalows",
        "property_ref": "Lakeside Tranquility Nordic Bungalow",
        "comment": (
            "I really wanted to negotiate the rent on the Wuse II bungalow by ₦400,000, but the platform locked the Deal Room "
            "because the landlord marked it as Fixed Price. Also had to wait 24 hours for Saturday inspection slots to open up."
        ),
        "date": "1 week ago",
    },
    {
        "id": 4,
        "user_name": "Engr. Tunde Bakare",
        "user_role": "Verified Landlord (Abuja & Lagos Portfolio)",
        "user_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "C of O, R of O & TDP Transparency Sold My Guzape Plot Fast",
        "property_ref": "Terra Crest Serviced Land Plot (600 SQM)",
        "comment": (
            "Buyers in Abuja always ask for C of O, R of O, and TDP costs before committing. Having those three documents "
            "broken down alongside the 5% land agency fee closed my Guzape land sale in 48 hours."
        ),
        "date": "1 week ago",
    },
    {
        "id": 5,
        "user_name": "Dr. Halima Yusuf",
        "user_role": "Verified Buyer (Katampe Extension, Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "impact_tag": "Saved ₦6M in the Deal Room & Smooth Escrow Handover",
        "property_ref": "Cedar Horizon Architectural Bungalow",
        "comment": (
            "The structured Deal Room timeline is miles better than endless WhatsApp chats. We agreed on a fair counter-offer "
            "and my funds stayed protected in Estate Escrow until the AGIS deed was handed over."
        ),
        "date": "2 weeks ago",
    },
    {
        "id": 6,
        "user_name": "Ibrahim Garba",
        "user_role": "Prospective Land Buyer (Lugbe, Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80",
        "rating": 2,
        "impact_tag": "7-Day Expiry Hid a Listing Before I Could Pay",
        "property_ref": "Centenary Greenbelt Residential Land",
        "comment": (
            "While I appreciate the anti-fraud verification, a property I was eyeing got temporarily flagged because the landlord "
            "was 1 day late on their 7-day reconfirmation timer, and customer support took 3 hours to reply to my ticket."
        ),
        "date": "3 weeks ago",
    },
    {
        "id": 7,
        "user_name": "Barr. Nkechi Eze",
        "user_role": "Verified Tenant (Maitama, Abuja)",
        "user_avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80",
        "rating": 4,
        "impact_tag": "Great Verification & Smart Property Matcher",
        "property_ref": "Serenity Pines Contemporary Duplex",
        "comment": (
            "Matched at 98% compatibility for my family in Maitama. Everything from the FCDA C of O check to the physical "
            "inspection was super professional."
        ),
        "date": "3 weeks ago",
    },
]

# ---------------------------------------------------------------------------
# 5. LANDLORD & TENANT ACCOUNTABILITY / COMPLAINT RESOLUTION SYSTEM
# ---------------------------------------------------------------------------
ACCOUNTABILITY_COMPLAINTS: list[dict[str, Any]] = [
    {
        "id": "CMP-2041",
        "filed_by_name": "Chidi Nwosu",
        "filed_by_role": "Tenant",
        "against_name": "Engr. Tunde Bakare",
        "against_role": "Landlord",
        "property_title": "Serenity Pines Contemporary Duplex (Maitama, Abuja)",
        "category": "Service Charge Reconciliation",
        "severity": "Medium",
        "description": "Requested itemized solar & backup diesel ledger for Q3 estate service charge.",
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
        "description": "Prospective tenant booked 10:00 AM Saturday physical inspection in Maitama but did not show up.",
        "status": "Under Review",
        "resolution_note": "Compliance team notified applicant; 1 attendance strike logged on applicant profile.",
        "reputation_impact": "Pending Admin Mediation",
        "created_at": "01 Nov 2026",
    },
    {
        "id": "CMP-2052",
        "filed_by_name": "Dr. Halima Yusuf",
        "filed_by_role": "Tenant",
        "against_name": "Unverified Third-Party Agent",
        "against_role": "Agent",
        "property_title": "Flagged Duplicate Listing in Wuse II (Removed)",
        "category": "Unauthorized Listing Attempt",
        "severity": "High",
        "description": "Reported an external agent attempting to re-upload photos of a verified Direct Landlord listing.",
        "status": "Resolved",
        "resolution_note": "Admin revoked agent access and locked listing under EST-VER-7430 Direct Landlord authority.",
        "reputation_impact": "Fake Ad Blocked Automatically",
        "created_at": "02 Nov 2026",
    },
]

# ---------------------------------------------------------------------------
# 6. TRANSACTION-SUPPORT NEGOTIATIONS ("DEAL ROOM" TIMELINES)
# ---------------------------------------------------------------------------
NEGOTIATIONS: dict[int, dict[str, Any]] = {
    1: {
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex (Maitama, Abuja)",
        "tenant_name": "Chidi Nwosu",
        "landlord_name": "Engr. Tunde Bakare",
        "listed_price": 10000000,
        "current_agreed_price": 9500000,
        "status": "Counter-Offer Active",
        "payment_tenure": "1 Year Annual Lease",
        "move_in_target": "15 Nov 2026",
        "events": [
            {
                "step": "01",
                "actor": "System Verification",
                "role": "system",
                "badge": "Authority Confirmed",
                "proposed_price": 10000000,
                "note": "Listing EST-VER-8821 in Maitama verified as Negotiable by Direct Landlord (Engr. Tunde Bakare).",
                "timestamp": "Yesterday, 09:15 AM",
            },
            {
                "step": "02",
                "actor": "Chidi Nwosu (Tenant)",
                "role": "tenant",
                "badge": "Initial Structured Offer",
                "proposed_price": 9200000,
                "note": "Ready to pay full commitment within 48 hours via Estate Escrow if we can close at ₦9,200,000/yr.",
                "timestamp": "Yesterday, 02:30 PM",
            },
            {
                "step": "03",
                "actor": "Engr. Tunde Bakare (Landlord)",
                "role": "landlord",
                "badge": "Landlord Counter-Offer",
                "proposed_price": 9500000,
                "note": "Appreciate your verified profile! I can approve ₦9,500,000/yr inclusive of exterior repainting before move-in.",
                "timestamp": "Today, 10:05 AM",
            },
        ],
    },
    4: {
        "property_id": 4,
        "property_title": "Terra Crest Serviced Land Plot (600 SQM, Guzape Abuja)",
        "tenant_name": "Chidi Nwosu",
        "landlord_name": "Engr. Tunde Bakare",
        "listed_price": 80000000,
        "current_agreed_price": 75000000,
        "status": "Accepted",
        "payment_tenure": "Outright Purchase (Escrow Protected)",
        "move_in_target": "Immediate Allocation",
        "events": [
            {
                "step": "01",
                "actor": "Chidi Nwosu (Tenant/Buyer)",
                "role": "tenant",
                "badge": "Purchase Offer",
                "proposed_price": 75000000,
                "note": "Offering ₦75,000,000 single-tranche settlement upon verification of C of O, R of O, and TDP.",
                "timestamp": "3 days ago",
            },
            {
                "step": "02",
                "actor": "Engr. Tunde Bakare (Landlord)",
                "role": "landlord",
                "badge": "Offer Accepted ✓",
                "proposed_price": 75000000,
                "note": "Offer accepted. Price locked at ₦75,000,000 for your checkout.",
                "timestamp": "2 days ago",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# 7. INSPECTIONS & TENANT APPLICATIONS
# ---------------------------------------------------------------------------
INSPECTIONS_AND_APPLICATIONS: list[dict[str, Any]] = [
    {
        "id": "INSP-501",
        "property_id": 1,
        "property_title": "Serenity Pines Contemporary Duplex",
        "location": "Maitama District, Abuja",
        "applicant_name": "Chidi Nwosu",
        "applicant_score": "4.95★ Verified Tenant",
        "preferred_date": "Saturday, 07 Nov 2026",
        "preferred_time": "11:00 AM",
        "inspection_type": "Physical On-Site Viewing",
        "application_status": "Approved for Selection",
        "note": "Pre-vetted income & NIN verified. Transparent 7% agency cost breakdown accepted.",
    },
    {
        "id": "INSP-502",
        "property_id": 3,
        "property_title": "Lakeside Tranquility Nordic Bungalow",
        "location": "Wuse II, Abuja",
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
        "location": "Asokoro District, Abuja",
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
# 8. HELP CENTER: FAQs & SUPPORT TICKETS
# ---------------------------------------------------------------------------
FAQS: list[dict[str, str]] = [
    {
        "category": "Verification & Anti-Fraud",
        "question": "How does Estate verify that a property is genuine and the advertiser has authority?",
        "answer": (
            "Every property displaying the 'Verified by Estate' shield goes through a 3-step check: "
            "(1) Title & ownership document verification (FCDA C of O, R of O, TDP, or Governor's Consent), "
            "(2) Signed Mandate or Direct Landlord identity match (NIN/CAC), and "
            "(3) On-site physical inspection with geo-tagged media."
        ),
    },
    {
        "category": "Transparent Charges",
        "question": "What is the Agency Fee rate for houses vs. land, and what land documents are included?",
        "answer": (
            "Agency fees on Estate are strictly capped at 7% for houses/apartments and 5% for land sales. "
            "For land listings, the Complete Cost Breakdown also explicitly itemizes Certificate of Occupancy (C of O), "
            "Right of Occupancy (R of O), and Title Deed Plan (TDP) charges upfront before you commit."
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
        "question": "Who is allowed to submit reviews for a property and its neighbourhood?",
        "answer": (
            "Only verified tenants and buyers who have completed payment for a property can submit a Property & Area "
            "Intelligence Review on that property's page. Once submitted, their feedback is automatically published "
            "to the Neighbourhood Intelligence hub."
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


def has_user_paid_for_property(property_id: int) -> bool:
    """Return True if the tenant has already paid for / checked out this property."""
    for tx in TENANT_RENTED_OR_BOUGHT:
        if tx["property_id"] == property_id:
            return True
    return False


def get_cart_ids(request: Request) -> list[int]:
    """Return list of property IDs currently selected in the tenant's checkout tray."""
    if "cart_ids" not in request.session:
        request.session["cart_ids"] = [1]
    return request.session["cart_ids"]


def get_effective_base_price(property_obj: Any) -> int:
    """Return negotiated price if an offer is Accepted in the Deal Room, else listed base_price."""
    neg = NEGOTIATIONS.get(property_obj.id)
    if neg and neg.get("status") == "Accepted":
        return int(neg["current_agreed_price"])
    return int(property_obj.base_price)


def get_flash_message(request: Request) -> dict[str, str] | None:
    """Pop and return one-time flash notification from session."""
    return request.session.pop("flash", None)


def set_flash_message(request: Request, title: str, kind: str = "success") -> None:
    request.session["flash"] = {"title": title, "kind": kind}
