from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Property(SQLModel, table=True):
    """
    SQLite database table for Property Listings (House & Land).
    Includes features for:
    - Verified property listings (authority, document proof, verification code)
    - Transparent rental/purchase charges (7% agency fee for houses, 5% for land, plus C of O, R of O, TDP for land)
    - Property update (7-day availability reconfirmation & status)
    - Neighbourhood intelligence linkage & metrics
    - Transaction-support service (negotiability & floor price)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(index=True, unique=True)
    category: str = Field(index=True)  # "Rent" or "Buy"
    property_type: str = Field(index=True)  # "Duplex", "Bungalow", "Apartment", "Land"
    location: str = Field(index=True)  # e.g. "Maitama District, Abuja"
    neighbourhood_key: str = Field(index=True)  # e.g. "maitama-abuja"
    address_hint: str

    bedrooms: int = Field(default=0)
    bathrooms: int = Field(default=0)
    size_sqm: int = Field(default=150)

    image_url: str
    secondary_image_url: str = Field(default="")
    description: str
    features_csv: str = Field(default="24/7 Security,Treated Water,Paved Roads,Smart Metering")

    # Verified property listings
    is_verified: bool = Field(default=True, index=True)
    verification_code: str = Field(default="EST-VER-0001")
    authority_role: str = Field(default="Direct Landlord")  # "Direct Landlord" or "Mandated Agent"
    authority_document: str = Field(default="FCDA Certificate of Occupancy (C of O) & AGIS Verified")
    inspected_by_estate: bool = Field(default=True)
    landlord_name: str = Field(default="Engr. Tunde Bakare")
    landlord_email: str = Field(default="landlord@estate.ng")
    landlord_reputation: float = Field(default=4.9)

    # Transparent rental/purchase charges (in NGN ₦)
    base_price: int = Field(default=4500000)  # Annual rent or outright purchase price
    price_period: str = Field(default="year")  # "year" for Rent, "outright" for Buy
    agency_fee: int = Field(default=315000)  # 7% for houses, 5% for land sale
    legal_fee: int = Field(default=225000)
    caution_deposit: int = Field(default=300000)
    service_charge: int = Field(default=400000)
    survey_or_deed_fee: int = Field(default=0)

    # Land-Specific Statutory Document Charges (C of O, R of O, TDP)
    c_of_o_fee: int = Field(default=0)  # Certificate of Occupancy (C of O)
    r_of_o_fee: int = Field(default=0)  # Right of Occupancy (R of O)
    tdp_fee: int = Field(default=0)     # Title Deed Plan (TDP)

    # Property update (7-day reconfirmation & availability)
    status: str = Field(default="Available", index=True)  # "Available", "Unavailable"
    last_confirmed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Neighbourhood intelligence summary metrics
    power_hours_per_day: int = Field(default=20)
    water_status: str = Field(default="Treated Central Borehole")
    drainage_score: float = Field(default=9.2)
    road_status: str = Field(default="Interlocked & Streetlit")
    security_score: float = Field(default=9.5)

    # Transaction-support service (Negotiation)
    is_negotiable: bool = Field(default=True)
    min_acceptable_price: int = Field(default=4000000)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def agency_fee_percent(self) -> int:
        return 5 if self.property_type == "Land" else 7

    @property
    def total_initial_commitment(self) -> int:
        """Complete upfront cost of securing the property before a tenant commits."""
        return (
            self.base_price
            + self.agency_fee
            + self.legal_fee
            + self.caution_deposit
            + self.service_charge
            + self.survey_or_deed_fee
            + self.c_of_o_fee
            + self.r_of_o_fee
            + self.tdp_fee
        )

    @property
    def additional_charges_total(self) -> int:
        return (
            self.agency_fee
            + self.legal_fee
            + self.caution_deposit
            + self.service_charge
            + self.survey_or_deed_fee
            + self.c_of_o_fee
            + self.r_of_o_fee
            + self.tdp_fee
        )

    @property
    def days_since_confirmed(self) -> int:
        now = datetime.now(timezone.utc)
        confirmed = self.last_confirmed_at
        if confirmed.tzinfo is None:
            confirmed = confirmed.replace(tzinfo=timezone.utc)
        delta = now - confirmed
        return max(0, delta.days)

    @property
    def days_until_reconfirmation_due(self) -> int:
        return max(0, 7 - self.days_since_confirmed)

    @property
    def is_reconfirmation_overdue(self) -> bool:
        return self.days_since_confirmed >= 7

    @property
    def features_list(self) -> list[str]:
        return [f.strip() for f in self.features_csv.split(",") if f.strip()]


class PropertyCreateSchema(BaseModel):
    """Pydantic schema for validating new property submissions from Landlords."""
    title: str
    category: str
    property_type: str
    location: str
    neighbourhood_key: str
    address_hint: str
    bedrooms: int = 0
    bathrooms: int = 0
    size_sqm: int = 150
    image_url: str
    description: str
    features_csv: str = "Gated Estate,Treated Water,Prepaid Meter,Dedicated Parking"
    authority_role: str = "Direct Landlord"
    authority_document: str = "FCDA C of O & Utility Proof"
    base_price: int
    agency_fee: int = 0
    legal_fee: int = 0
    caution_deposit: int = 0
    service_charge: int = 0
    survey_or_deed_fee: int = 0
    c_of_o_fee: int = 0
    r_of_o_fee: int = 0
    tdp_fee: int = 0
    is_negotiable: bool = True
    min_acceptable_price: int = 0
    power_hours_per_day: int = 20
    water_status: str = "FCT Water Board + Borehole"
    drainage_score: float = 9.2
    road_status: str = "Tarred Access Road"
    security_score: float = 9.4
