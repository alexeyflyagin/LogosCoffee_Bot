from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AdminAccountEntity(BaseModel):
    id: int
    token: str
    date_last_announcement_distributing: datetime | None

    model_config = ConfigDict(from_attributes=True)


class EmployeeAccountEntity(BaseModel):
    id: int
    token: str

    model_config = ConfigDict(from_attributes=True)


class ClientAccountEntity(BaseModel):
    id: int
    token: str
    client_name: str | None
    phone_number: str
    date_create: datetime
    loyalty_points: int
    date_last_review: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ReviewEntity(BaseModel):
    id: int
    date_create: datetime
    text_content: str

    model_config = ConfigDict(from_attributes=True)


class AnnouncementEntity(BaseModel):
    id: int
    date_create: datetime
    date_last_distribute: datetime | None
    text_content: str | None
    preview_photo_data: str | None

    model_config = ConfigDict(from_attributes=True)


class UserStateEntity(BaseModel):
    id: int
    bot_id: int
    user_id: int
    chat_id: int
    state: str | None
    data: dict

    model_config = ConfigDict(from_attributes=True)


class EventSubscriberEntity(BaseModel):
    id: int
    event_name: str
    date_create: datetime
    chat_id: int
    data: dict[str, Any] | None

    model_config = ConfigDict(from_attributes=True)


class OrderEntity(BaseModel):
    id: int
    date_create: datetime
    client_id: int
    pickup_code: str | None
    date_pending: datetime | None
    date_cooking: datetime | None
    date_ready: datetime | None
    date_completed: datetime | None
    date_canceled: datetime | None
    cancel_details: str | None
    details: str | None

    model_config = ConfigDict(from_attributes=True)
