from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, Session, create_engine, select
from app.models import Property

SQLITE_FILE_NAME = "estate.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


def init_db_and_seed():
    """Create SQLite tables and seed initial verified & sample properties (majority in Abuja)."""
    SQLModel.metadata.create_all(engine)
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        existing = session.exec(select(Property)).first()
        if existing:
            return

        seed_properties = [
            # 1. Maitama, Abuja (House - Rent, 7% Agency Fee)
            Property(
                title="Serenity Pines Contemporary Duplex",
                slug="serenity-pines-contemporary-duplex",
                category="Rent",
                property_type="Duplex",
                location="Maitama District, Abuja",
                neighbourhood_key="maitama-abuja",
                address_hint="Off Gana Street, Maitama, Abuja",
                bedrooms=4,
                bathrooms=4,
                size_sqm=360,
                image_url="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Architectural 4-bedroom semi-detached duplex in Maitama with timber slat facade, double-volume living area, "
                    "fitted Bosch kitchen, and private courtyard. Physically inspected and AGIS title-verified by Estate."
                ),
                features_csv="23hrs AEDC Priority Power,FCT Water Board + Borehole,Biometric Access,Fitted Kitchen,BQ Included,Flood-Free Storm Drain",
                is_verified=True,
                verification_code="EST-VER-8821",
                authority_role="Direct Landlord",
                authority_document="FCDA Certificate of Occupancy (C of O) & AGIS Match",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=10000000,
                price_period="year",
                agency_fee=700000,  # Exactly 7% of 10,000,000
                legal_fee=500000,
                caution_deposit=500000,
                service_charge=650000,
                survey_or_deed_fee=0,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Available",
                last_confirmed_at=now - timedelta(days=1),
                power_hours_per_day=23,
                water_status="FCT Water Board + Triple Filtration",
                drainage_score=9.7,
                road_status="Express-Grade Asphalt & Solar Streetlights",
                security_score=9.8,
                is_negotiable=True,
                min_acceptable_price=9200000,
            ),
            # 2. Asokoro, Abuja (House - Buy, 7% Agency Fee)
            Property(
                title="Prairie Vista Glass Villa",
                slug="prairie-vista-glass-villa",
                category="Buy",
                property_type="Duplex",
                location="Asokoro District, Abuja",
                neighbourhood_key="asokoro-abuja",
                address_hint="Nelson Mandela Street Axis, Asokoro, Abuja",
                bedrooms=5,
                bathrooms=6,
                size_sqm=640,
                image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Ultra-luxury 5-bedroom detached diplomatic residence in Asokoro featuring floor-to-ceiling low-E glass, "
                    "private lap pool, cinema room, and smart home automation. Direct sale with verified FCDA Certificate of Occupancy."
                ),
                features_csv="24/7 Uninterrupted Power,Swimming Pool,Home Cinema,Smart Automation,2-Room BQ,Diplomatic Zone Patrol",
                is_verified=True,
                verification_code="EST-VER-9104",
                authority_role="Direct Landlord",
                authority_document="FCDA Certificate of Occupancy (C of O) #FCT-44912",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=280000000,
                price_period="outright",
                agency_fee=19600000,  # Exactly 7% of 280,000,000
                legal_fee=5600000,
                caution_deposit=0,
                service_charge=0,
                survey_or_deed_fee=3500000,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Available",
                last_confirmed_at=now - timedelta(days=2),
                power_hours_per_day=24,
                water_status="Lower Usuma Dam Mains + UV Filtration",
                drainage_score=9.9,
                road_status="Dual-Carriageway Diplomatic Boulevard",
                security_score=9.9,
                is_negotiable=True,
                min_acceptable_price=265000000,
            ),
            # 3. Wuse II, Abuja (House - Rent, 7% Agency Fee)
            Property(
                title="Lakeside Tranquility Nordic Bungalow",
                slug="lakeside-tranquility-nordic-bungalow",
                category="Rent",
                property_type="Bungalow",
                location="Wuse II, Abuja",
                neighbourhood_key="wuse-2-abuja",
                address_hint="Off Aminu Kano Crescent, Wuse II, Abuja",
                bedrooms=3,
                bathrooms=3,
                size_sqm=280,
                image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Modern single-story 3-bedroom Scandinavian-inspired bungalow set in a serene, tree-lined close in Wuse II. "
                    "Zero hidden fees, clear 7% agency breakdown and service commitments prior to inspection."
                ),
                features_csv="22hrs Band-A Power,Private Garden,Solar Inverter Backup,Quiet Close,3 Car Park,Verified Landlord",
                is_verified=True,
                verification_code="EST-VER-7430",
                authority_role="Direct Landlord",
                authority_document="AGIS Registered Deed & FCDA Recertification",
                inspected_by_estate=True,
                landlord_name="Alhaji Musa Danjuma",
                landlord_email="musa@estate.ng",
                landlord_reputation=4.95,
                base_price=6000000,
                price_period="year",
                agency_fee=420000,  # Exactly 7% of 6,000,000
                legal_fee=300000,
                caution_deposit=350000,
                service_charge=300000,
                survey_or_deed_fee=0,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Available",
                last_confirmed_at=now - timedelta(days=3),
                power_hours_per_day=22,
                water_status="FCT Water Board + Borehole Softener",
                drainage_score=9.5,
                road_status="Tarred & Tree-Lined Crescent",
                security_score=9.6,
                is_negotiable=False,
                min_acceptable_price=6000000,
            ),
            # 4. Guzape Hills, Abuja (Land - Buy, 5% Agency Fee + C of O, R of O, TDP)
            Property(
                title="Terra Crest Serviced Land Plot (600 SQM)",
                slug="terra-crest-serviced-land-plot-600sqm",
                category="Buy",
                property_type="Land",
                location="Guzape District, Abuja",
                neighbourhood_key="guzape-abuja",
                address_hint="Guzape Hills Diplomatic Enclave, Abuja",
                bedrooms=0,
                bathrooms=0,
                size_sqm=600,
                image_url="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=900&q=80",
                description=(
                    "100% dry, rock-solid perimeter-fenced 600 SQM residential plot overlooking Guzape Hills. "
                    "Includes full FCDA Certificate of Occupancy (C of O), Right of Occupancy (R of O), and Title Deed Plan (TDP) verification."
                ),
                features_csv="FCDA C of O + R of O + TDP Ready,100% Dry Elevated Plot,Underground Cabling,Instant Allocation,Tarred Hilltop Access",
                is_verified=True,
                verification_code="EST-VER-6619",
                authority_role="Mandated Agent",
                authority_document="FCDA C of O, R of O & AGIS Title Deed Plan (TDP)",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=80000000,
                price_period="outright",
                agency_fee=4000000,  # Exactly 5% of 80,000,000 for Land Sale
                legal_fee=1600000,
                caution_deposit=0,
                service_charge=0,
                survey_or_deed_fee=0,
                c_of_o_fee=2500000,  # C of O documentation fee
                r_of_o_fee=1200000,  # R of O documentation fee
                tdp_fee=800000,      # TDP (Title Deed Plan) fee
                status="Available",
                last_confirmed_at=now - timedelta(days=4),
                power_hours_per_day=22,
                water_status="FCT Trunk Mains Connection Ready",
                drainage_score=9.6,
                road_status="Asphalt Hilltop Boulevard",
                security_score=9.7,
                is_negotiable=True,
                min_acceptable_price=74000000,
            ),
            # 5. Jabi Lake Axis, Abuja (Apartment - Rent, 7% Agency Fee)
            Property(
                title="Charm Manor Minimalist Loft Apartment",
                slug="charm-manor-minimalist-loft-apartment",
                category="Rent",
                property_type="Apartment",
                location="Jabi Lake Axis, Abuja",
                neighbourhood_key="jabi-abuja",
                address_hint="Bala Sokoto Way, Jabi, Abuja",
                bedrooms=2,
                bathrooms=2,
                size_sqm=135,
                image_url="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Bright 2-bedroom architectural apartment 3 minutes from Jabi Lake Mall. "
                    "Features fiber-to-the-home internet conduit, solar inverter backup, and transparent 7% agency fee."
                ),
                features_csv="Fiber Optic Ready,20hrs Band-A Power,Prepaid Sub-Meter,CCTV Surveillance,Dedicated Parking",
                is_verified=True,
                verification_code="EST-VER-5502",
                authority_role="Direct Landlord",
                authority_document="AGIS Title Certificate & Signed Landlord Mandate",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=4000000,
                price_period="year",
                agency_fee=280000,  # Exactly 7% of 4,000,000
                legal_fee=200000,
                caution_deposit=250000,
                service_charge=300000,
                survey_or_deed_fee=0,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Available",
                last_confirmed_at=now - timedelta(days=5),
                power_hours_per_day=20,
                water_status="FCT Water Board + Borehole",
                drainage_score=9.3,
                road_status="Tarred Street with Covered Drains",
                security_score=9.4,
                is_negotiable=True,
                min_acceptable_price=3600000,
            ),
            # 6. Katampe Extension, Abuja (Bungalow - Buy, 7% Agency Fee)
            Property(
                title="Cedar Horizon Architectural Bungalow",
                slug="cedar-horizon-architectural-bungalow",
                category="Buy",
                property_type="Bungalow",
                location="Katampe Extension, Abuja",
                neighbourhood_key="katampe-abuja",
                address_hint="Diplomatic Enclave, Katampe Extension, Abuja",
                bedrooms=4,
                bathrooms=4,
                size_sqm=410,
                image_url="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Contemporary 4-bedroom detached bungalow on an expansive landscaped plot in Katampe Extension. "
                    "Designed with warm cedar soffits, cantilevered carport, and full AGIS title verification."
                ),
                features_csv="AGIS Verified Title,22hrs Power Supply,Solar Hybrid Array,Landscaped Courtyard,Security Gatehouse",
                is_verified=True,
                verification_code="EST-VER-9910",
                authority_role="Direct Landlord",
                authority_document="FCDA Certificate of Occupancy & AGIS Search Report",
                inspected_by_estate=True,
                landlord_name="Alhaji Musa Danjuma",
                landlord_email="musa@estate.ng",
                landlord_reputation=4.95,
                base_price=140000000,
                price_period="outright",
                agency_fee=9800000,  # Exactly 7% of 140,000,000
                legal_fee=2800000,
                caution_deposit=0,
                service_charge=0,
                survey_or_deed_fee=1800000,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Available",
                last_confirmed_at=now - timedelta(days=2),
                power_hours_per_day=22,
                water_status="FCT Water Board + Borehole",
                drainage_score=9.6,
                road_status="Express-Grade Asphalt",
                security_score=9.7,
                is_negotiable=True,
                min_acceptable_price=132000000,
            ),
            # 7. Lugbe / Airport Road Corridor, Abuja (Land - Buy, 5% Agency Fee + C of O, R of O, TDP)
            Property(
                title="Centenary Greenbelt Residential Land (1000 SQM)",
                slug="centenary-greenbelt-land-1000sqm",
                category="Buy",
                property_type="Land",
                location="Airport Road / Lugbe, Abuja",
                neighbourhood_key="lugbe-abuja",
                address_hint="Centenary City Axis, Airport Road, Abuja",
                bedrooms=0,
                bathrooms=0,
                size_sqm=1000,
                image_url="https://images.unsplash.com/photo-1500076656116-558758c991c1?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Full 1,000 SQM dry residential land plot along the Nnamdi Azikiwe International Airport corridor in Abuja. "
                    "Includes verified FCDA Right of Occupancy (R of O), Certificate of Occupancy (C of O) processing, and AGIS Title Deed Plan (TDP)."
                ),
                features_csv="C of O + R of O + TDP Included,100% Dry Table Land,Perimeter Gatehouse,10-Lane Airport Expressway",
                is_verified=True,
                verification_code="EST-VER-3109",
                authority_role="Mandated Agent",
                authority_document="FCDA R of O, C of O & AGIS Title Deed Plan (TDP)",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=25000000,
                price_period="outright",
                agency_fee=1250000,  # Exactly 5% of 25,000,000 for Land Sale
                legal_fee=500000,
                caution_deposit=0,
                service_charge=0,
                survey_or_deed_fee=0,
                c_of_o_fee=1200000,  # C of O fee
                r_of_o_fee=650000,   # R of O fee
                tdp_fee=450000,      # TDP fee
                status="Available",
                last_confirmed_at=now - timedelta(days=4),
                power_hours_per_day=19,
                water_status="Central Estate Borehole Network",
                drainage_score=9.1,
                road_status="10-Lane Airport Expressway Frontage",
                security_score=9.2,
                is_negotiable=True,
                min_acceptable_price=23000000,
            ),
            # 8. Lekki Phase 1, Lagos (Already Rented / Paid by Demo Tenant - House, 7% Agency Fee)
            Property(
                title="Veranda Court Serviced 3-Bed Terrace",
                slug="veranda-court-serviced-3bed-terrace",
                category="Rent",
                property_type="Duplex",
                location="Lekki Phase 1, Lagos",
                neighbourhood_key="lekki-phase-1",
                address_hint="Off Admiralty Way, Lekki Phase 1, Lagos",
                bedrooms=3,
                bathrooms=4,
                size_sqm=230,
                image_url="https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=1200&q=85",
                secondary_image_url="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=900&q=80",
                description=(
                    "Recently rented 3-bedroom terrace duplex demonstrating Estate's 7-day availability policy: "
                    "marked Unavailable immediately after tenant checkout so prospective renters never pay fake inspection fees."
                ),
                features_csv="Marked Unavailable After Checkout,20hrs Estate Power,Gym & Pool Access,Verified Landlord",
                is_verified=True,
                verification_code="EST-VER-4012",
                authority_role="Direct Landlord",
                authority_document="Governor's Consent Verified",
                inspected_by_estate=True,
                landlord_name="Engr. Tunde Bakare",
                landlord_email="landlord@estate.ng",
                landlord_reputation=4.9,
                base_price=6000000,
                price_period="year",
                agency_fee=420000,  # Exactly 7% of 6,000,000
                legal_fee=300000,
                caution_deposit=400000,
                service_charge=500000,
                survey_or_deed_fee=0,
                c_of_o_fee=0,
                r_of_o_fee=0,
                tdp_fee=0,
                status="Unavailable",
                last_confirmed_at=now - timedelta(days=8),
                power_hours_per_day=20,
                water_status="Central Treated Water",
                drainage_score=9.1,
                road_status="Interlocked Estate Road",
                security_score=9.4,
                is_negotiable=False,
                min_acceptable_price=6000000,
            ),
        ]

        for prop in seed_properties:
            session.add(prop)
        session.commit()
