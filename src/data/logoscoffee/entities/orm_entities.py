from datetime import datetime

from attr import dataclass
from pydantic import BaseModel


@dataclass
class AdminAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None

    class Config:
        from_attributes = True

@dataclass
class EmployeeAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None

    class Config:
        from_attributes = True

@dataclass
class ClientAccountEntity(BaseModel):
    id: int
    client_name: str | None
    phone_number: str
    date_create: datetime
    loyalty_points: int
    date_last_review: datetime | None

    class Config:
        from_attributes = True

@dataclass
class ReviewEntity(BaseModel):
    id: int
    date_create: datetime
    text_content: str

    class Config:
        from_attributes = True

@dataclass
class PromotionalOfferEntity(BaseModel):
    id: int
    date_create: datetime
    date_start: datetime | None
    text_content: str | None
    preview_photo: str | None

    class Config:
        from_attributes = True

@dataclass
class UserStateEntity(BaseModel):
    id: int
    bot_id: int
    user_id: int
    chat_id: int
    state: str
    data: dict

    class Config:
        from_attributes = True


@dataclass
class EventSubscriberEntity(BaseModel):
    id: int
    event_name: str
    date_create: datetime
    chat_id: int

    class Config:
        from_attributes = True