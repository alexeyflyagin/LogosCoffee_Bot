from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError
from src.data.logoscoffee.interfaces.admin_menu_service import AdminMenuService
from src.presentation.bots.admin_bot import keyboards
from src.presentation.bots.client_bot import commands
from src.presentation.bots.client_bot.handlers.utils import unknown_error
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.bots.utils import send_or_update_msg
from src.presentation.resources import strings

router = Router(name=__name__)
menu_service: AdminMenuService


@router.message(MainStates(), F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    await show_menu(msg, state)


async def show_menu(msg: Message, state: FSMContext):
    try:
        menu = await menu_service.get_menu()
        text = menu.text_content or strings.ADMIN.EMPTY_MENU_CONTENT
        await send_or_update_msg(msg, text=text, replay_markup=keyboards.EMPTY_MENU_IK)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.exception(e)
        await unknown_error(msg, state)
