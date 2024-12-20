from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


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

    product_and_orders_rs: list['ProductAndOrderEntity'] = None

    model_config = ConfigDict(from_attributes=True)

    class OrderState(Enum):
        DRAFT = 0
        PENDING = 1
        COOKING = 2
        READY = 3
        COMPLETED = 4
        CANCELED = 5

    @property
    def state(self) -> OrderState:
        if self.date_canceled:
            return self.OrderState.CANCELED
        if self.date_completed:
            return self.OrderState.COMPLETED
        if self.date_ready:
            return self.OrderState.READY
        if self.date_cooking:
            return self.OrderState.COOKING
        if self.date_pending:
            return self.OrderState.PENDING
        else:
            return self.OrderState.DRAFT

    @property
    def product_and_order_groups(self) -> list[list['ProductAndOrderEntity']] | None:
        if self.product_and_orders_rs is None:
            return None
        groups = defaultdict(list)
        for item in self.product_and_orders_rs:
            groups[item.product_rs.id].append(item)
        res = list(groups.values())
        return res

    @property
    def total_price(self) -> Decimal | None:
        if self.product_and_orders_rs is None:
            return None
        if self.state == self.OrderState.DRAFT:
            return sum([i.product_rs.price for i in self.product_and_orders_rs], Decimal('0'))
        else:
            return sum([i.product_price for i in self.product_and_orders_rs], Decimal('0'))

class ProductAndOrderEntity(BaseModel):
    id: int
    date_create: datetime
    order_id: int
    product_id: int
    product_price: Decimal | None

    product_rs: 'ProductEntity' = None
    order_rs: 'OrderEntity' = None

    model_config = ConfigDict(from_attributes=True)

class ProductEntity(BaseModel):
    id: int
    date_create: datetime
    is_available: bool
    price: Decimal
    product_name: str
    description: str
    preview_photo: str | None

    product_and_orders_rs: 'ProductAndOrderEntity' = None

    model_config = ConfigDict(from_attributes=True)

class AdminAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None
    date_last_announcement_distributing: datetime | None

    model_config = ConfigDict(from_attributes=True)

class EmployeeAccountEntity(BaseModel):
    id: int
    key: str
    date_authorized: datetime | None

    model_config = ConfigDict(from_attributes=True)

class ClientAccountEntity(BaseModel):
    id: int
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
    preview_photo: str | None

    model_config = ConfigDict(from_attributes=True)

class UserStateEntity(BaseModel):
    id: int
    bot_id: int
    user_id: int
    chat_id: int
    state: str
    data: dict

    model_config = ConfigDict(from_attributes=True)

class EventSubscriberEntity(BaseModel):
    id: int
    event_name: str
    date_create: datetime
    chat_id: int

    model_config = ConfigDict(from_attributes=True)