from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Result:
    message: str
    status: str
    data: Optional [List[Dict]] = None

@dataclass
class Address:
    city: Optional[str] = None
    country: Optional[str] = None
    id: Optional[int] = None
    is_default: Optional[bool] = None
    postal_code: Optional[str] = None
    province: Optional[str] = None
    state: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    type: Optional[str] = None


@dataclass
class EmailAddress:
    address: Optional[str] = None
    id: Optional[int] = None
    is_default: Optional[bool] = None
    type: Optional[str] = None


@dataclass
class Phone:
    extension: Optional[str] = None
    id: Optional[int] = None
    is_default: Optional[bool] = None
    number: Optional[str] = None
    type: Optional[str] = None


@dataclass
class Guest:
    addresses: Optional[List[Address]] = None
    email_addresses: Optional[List[EmailAddress]] = None
    first_name: Optional[str] = None
    id: Optional[int] = None
    last_name: Optional[str] = None
    notes: Optional[str] = None
    phones: Optional[List[Phone]] = None



@dataclass
class Property:
    active: Optional[bool] = None
    address: Optional[Address] = None
    bathrooms: Optional[int] = None
    bathrooms_full: Optional[int] = None
    bathrooms_half: Optional[int] = None
    bedrooms: Optional[int] = None
    check_in: Optional[str] = None
    check_in_end: Optional[str] = None
    check_out: Optional[str] = None
    currency_code: Optional[str] = None
    display_order: Optional[int] = None
    external_display_order: Optional[int] = None
    external_name: Optional[str] = None
    id: Optional[int] = None
    internal_code: Optional[str] = None
    key: Optional[UUID] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    max_adults: Optional[int] = None
    max_children: Optional[int] = None
    max_guests: Optional[int] = None
    max_pets: Optional[int] = None
    name: Optional[str] = None
    owner_id: Optional[int] = None
    property_type: Optional[str] = None
    public_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_url_large: Optional[str] = None
    thumbnail_url_medium: Optional[str] = None



@dataclass
class Charge:
    amount: Optional[int] = None
    commission_amount: Optional[int] = None
    description: Optional[str] = None
    expense_id: Optional[int] = None
    is_channel_managed: Optional[bool] = None
    is_commission_all: Optional[bool] = None
    is_expense_all: Optional[bool] = None
    is_taxable: Optional[bool] = None
    owner_amount: Optional[int] = None
    owner_commission_percent: Optional[int] = None
    position: Optional[int] = None
    rate: Optional[int] = None
    rate_is_percent: Optional[bool] = None
    surcharge_id: Optional[int] = None
    tax_id: Optional[int] = None
    type: Optional[str] = None


@dataclass
class DoorCode:
    code: Optional[str] = None
    lock_names: Optional[str] = None



@dataclass
class Booking:
    adults: Optional[int] = None
    arrival: Optional[datetime] = None
    booked_utc: Optional[datetime] = None
    canceled_utc: Optional[datetime] = None
    charges: Optional[List[Charge]] = None
    check_in: Optional[str] = None
    check_in_end: Optional[str] = None
    check_out: Optional[str] = None
    children: Optional[int] = None
    cleaning_date: Optional[datetime] = None
    currency_code: Optional[str] = None
    departure: Optional[datetime] = None
    door_codes: Optional[List[DoorCode]] = None
    form_key: Optional[str] = None
    guest: Optional[Guest] = None
    guest_id: Optional[int] = None
    id: Optional[int] = None
    infants: Optional[int] = None
    is_block: Optional[bool] = None
    listing_site: Optional[str] = None
    notes: Optional[str] = None
    owner_id: Optional[int] = None
    pending_until_utc: Optional[datetime] = None
    pets: Optional[int] = None
    platform_email_address: Optional[str] = None
    platform_reservation_number: Optional[str] = None
    property: Optional[Property] = None
    property_id: Optional[int] = None
    quote_id: Optional[int] = None
    status: Optional[str] = None
    title: Optional[str] = None
    thread_ids: Optional[List[int]] = None
    total_amount: Optional[int] = None
    total_host_fees: Optional[int] = None
    total_owed: Optional[int] = None
    total_paid: Optional[int] = None
    total_refunded: Optional[int] = None
    type: Optional[str] = None
    updated_utc: Optional[datetime] = None
    cancellation_policy_description: Optional[str] = None
    created_utc: Optional[datetime] = None