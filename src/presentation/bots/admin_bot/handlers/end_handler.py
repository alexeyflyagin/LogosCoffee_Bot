from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.exceptions import InvalidToken, DatabaseError, UnknownError
from src.data.logoscoffee.interfaces import admin_service
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import keyboards
from src.presentation.bots.admin_bot.handlers.utils import get_token, invalid_token_error, unknown_error
from src.presentation.bots.admin_bot.states import MainStates
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(MainStates.Main)
async def other_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        await admin_service.validate_token(token)
        await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)
