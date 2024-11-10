from datetime import datetime

from attr import dataclass
from pydantic import BaseModel


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
    preview_photo_url: str | None

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
class EventSubscriberEntity:
    id: int
    event_name: str
    date_create: datetime
    user_state_id: int
    user_state: UserStateEntity