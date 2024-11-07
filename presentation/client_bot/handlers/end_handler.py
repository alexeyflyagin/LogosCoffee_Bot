from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.services.client_service import client_service
from data.services.exceptions import InvalidToken, DatabaseError, UnknownError
from presentation import strings
from presentation.client_bot import keyboards
from presentation.client_bot.handlers.utils import get_token, invalid_token_error, unknown_error
from presentation.client_bot.states import MainStates

router = Router()


@router.message(MainStates.Main)
async def other_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        await client_service.validate_token(token)
        await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)
