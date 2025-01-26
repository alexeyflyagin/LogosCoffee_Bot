from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.loggers import bot_logger as logger
from src.presentation.bots import constants
from src.presentation.bots.client_bot.handlers.utils import unknown_error
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.bots.views.client.models.menu import MenuViewData
from src.presentation.resources import strings

router = Router(name=__name__)
client_service: ClientService


@router.message(MainStates(), F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    try:
        menu = await client_service.get_menu()
        await MenuViewData.from_entity(menu).view().answer_view(msg)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.exception(e)
        await unknown_error(msg, state)


@router.callback_query(F.data == constants.CALLBACK_DATA__LIST_MENU)
async def menu_handler(callback: CallbackQuery, state: FSMContext):
    try:
        menu = await client_service.get_menu()
        await MenuViewData.from_entity(menu).view().answer_view(callback.message)
        await callback.answer()
    except (DatabaseError, UnknownError, Exception) as e:
        logger.exception(e)
        await unknown_error(callback.message, state)
