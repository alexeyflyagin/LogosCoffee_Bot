from datetime import datetime

from pydantic import BaseModel

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.enums import OrderStateGroup, OrderState


class OrderViewData(BaseModel):
    id: int
    date_create: datetime
    client_id: int
    pickup_code: str | None
    cancel_details: str | None
    details: str | None
    client_nickname: str | None
    state: OrderState
    state_group: OrderStateGroup

    @staticmethod
    def from_order_entity(order_entity: OrderEntity) -> "OrderViewData":
        if not isinstance(order_entity, OrderEntity):
            raise ValueError("Incorrect type of the args.")

        if not order_entity.client:
            raise ValueError("The OrderEntity is required a `client` field.")

        return OrderViewData(
            id=order_entity.id,
            date_create=order_entity.date_create,
            client_id=order_entity.client_id,
            pickup_code=order_entity.pickup_code,
            cancel_details=order_entity.cancel_details,
            details=order_entity.details,
            client_nickname=order_entity.client.client_name,
            state=order_entity.state,
            state_group=order_entity.state_group,
        )
