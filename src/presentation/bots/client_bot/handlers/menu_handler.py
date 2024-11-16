from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.bots.client_bot.handlers.utils import unknown_error
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.bots.utils import send_or_update_msg
from src.presentation.resources import strings

router = Router()
client_service: ClientService


@router.message(MainStates.Main, F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    try:
        await show_menu(msg)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


async def show_menu(msg: Message, is_update: bool = False):
    products = await client_service.get_menu()
    all_products_s = []
    for i in range(len(products.all_products)):
        all_products_s.append(strings.CLIENT.MENU.ITEM.format(
            index=i + 1,
            product_name=products.all_products[i].product_name,
            price=f"{products.all_products[i].price:.2f} ₽"
        ))
    text = strings.CLIENT.MENU.PAGE.format(items='\n'.join(all_products_s))
    await send_or_update_msg(msg, text=text, is_update=is_update)