from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.entities.orm_entities import ProductEntity, ProductAndOrderEntity
from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, InvalidTokenError
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.presentation.bots.client_bot.handlers.utils import invalid_token_error
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.constants import TAG__DRAFT_ORDER
from src.presentation.bots.client_bot.handlers.utils import unknown_error, get_token
from src.presentation.bots.currency_formatter import to_rub
from src.presentation.bots.list_markup import ListItem, get_pages, list_keyboard
from src.presentation.bots.utils import send_or_update_msg
from src.presentation.resources import strings

router = Router()
order_service: ClientOrderService


@router.message(F.text == strings.BTN.DRAFT_ORDER)
async def draft_order_handler(msg: Message, state: FSMContext):
    await show_draft_order(msg, state)


async def show_draft_order(msg: Message, state: FSMContext, pg_index: int = 0, is_update: bool = False):
    text = strings.CLIENT.DRAFT_ORDER.MAIN_EMPTY
    try:
        token = await get_token(state)
        draft_order = await order_service.get_draft_order(token)
        product_and_order_groups = draft_order.product_and_order_groups
        if not product_and_order_groups:
            await send_or_update_msg(msg, text, is_update=is_update, replay_markup=keyboards.EMPTY_DRAFT_ORDER_KEYBOARD)
            return

        items = []
        for i in range(len(product_and_order_groups)):
            product_id = product_and_order_groups[i][0].product_id
            items.append(ListItem(str(i + 1), product_id, product_and_order_groups[i]))
        pages = get_pages(items)
        markup = list_keyboard(tag=TAG__DRAFT_ORDER, pg_index=pg_index, pg_count=len(pages), pg_items=pages[pg_index],
                               add_btn_text=None, back_btn_text=None)

        items_str = []
        for item in pages[pg_index]:
            product_and_order: ProductAndOrderEntity = item.obj[0]
            product: ProductEntity = product_and_order.product_rs
            count = len(item.obj)
            items_str.append(strings.CLIENT.DRAFT_ORDER.ITEM.format(
                index=item.name,
                product_name=product.product_name,
                price=to_rub(product.price),
                counter=strings.CLIENT.DRAFT_ORDER.ITEM_COUNTER.format(counter=count) if count > 1 else "",
            ))

        text = strings.CLIENT.DRAFT_ORDER.MAIN.format(
            items='\n'.join(items_str),
            total_price=to_rub(draft_order.total_price)
        )
        await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=markup)
    except InvalidTokenError:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)
