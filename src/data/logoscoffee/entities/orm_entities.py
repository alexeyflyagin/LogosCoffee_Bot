from datetime import datetime
from decimal import Decimal

from attr import dataclass
from pydantic import BaseModel, ConfigDict


@dataclass
class OrderEntity(BaseModel):
    pass # TODO

    model_config = ConfigDict(from_attributes = True)

@dataclass
class ProductEntity(BaseModel):
    id: int
    date_create: datetime
    is_available: bool
    price: Decimal
    product_name: str
    description: str
    preview_photo: str | None

    model_config = ConfigDict(from_attributes = True)

@dataclass
class AdminAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None
    date_last_offer_distributing: datetime | None

    model_config = ConfigDict(from_attributes = True)

@dataclass
class EmployeeAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None

    model_config = ConfigDict(from_attributes = True)

@dataclass
class ClientAccountEntity(BaseModel):
    id: int
    client_name: str | None
    phone_number: str
    date_create: datetime
    loyalty_points: int
    date_last_review: datetime | None

    model_config = ConfigDict(from_attributes = True)

@dataclass
class ReviewEntity(BaseModel):
    id: int
    date_create: datetime
    text_content: str

    model_config = ConfigDict(from_attributes = True)

@dataclass
class PromotionalOfferEntity(BaseModel):
    id: int
    date_create: datetime
    date_last_distribute: datetime | None
    text_content: str | None
    preview_photo: str | None

    model_config = ConfigDict(from_attributes = True)

@dataclass
class UserStateEntity(BaseModel):
    id: int
    bot_id: int
    user_id: int
    chat_id: int
    state: str
    data: dict

    model_config = ConfigDict(from_attributes = True)


@dataclass
class EventSubscriberEntity(BaseModel):
    id: int
    event_name: str
    date_create: datetime
    chat_id: int

    model_config = ConfigDict(from_attributes = True)