from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel


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
