from datetime import datetime
from html import escape

from aiogram.enums import ParseMode
from pydantic import BaseModel

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.enums import OrderStateGroup, OrderState
from src.presentation.bots.views.employee.keyboards.order import order_ikm
from src.presentation.bots.views.models import View, ViewType
from src.presentation.resources import strings


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

    @property
    def state_str(self) -> str:
        if self.state == OrderState.PENDING:
            return strings.EMPLOYEE.ORDER.STATES.PENDING
        elif self.state == OrderState.COOKING:
            return strings.EMPLOYEE.ORDER.STATES.COOKING
        elif self.state == OrderState.READY and self.pickup_code:
            return strings.EMPLOYEE.ORDER.STATES.READY.format(code=self.pickup_code)
        elif self.state == OrderState.COMPLETED:
            return strings.EMPLOYEE.ORDER.STATES.COMPLETED
        elif self.state == OrderState.CANCELED and self.cancel_details:
            return strings.EMPLOYEE.ORDER.STATES.CANCELED.format(cancel_details=escape(self.cancel_details))
        else:
            raise ValueError('Unexpected order state.')

    def view(self) -> View:
        if self.state_group == OrderStateGroup.IN_PROGRESS:
            text = strings.EMPLOYEE.ORDER.IN_PROGRESS_VIEW
        elif self.state_group == OrderStateGroup.CLOSED:
            text = strings.EMPLOYEE.ORDER.CLOSED_VIEW
        else:
            raise ValueError('Unexpected order state group.')

        text = text.format(
            id=self.id,
            state=self.state_str,
            nickname=escape(self.client_nickname) if self.client_nickname else strings.EMPLOYEE.ORDER.NO_NICKNAME,
            client_id=self.client_id,
            date=self.date_create.strftime('%d.%m.%Y %H:%M:%S'),
            details=escape(self.details),
        )
        markup = order_ikm(self.id, self.state_group, self.state)

        return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.HTML, reply_markup=markup)
