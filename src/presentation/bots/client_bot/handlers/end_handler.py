from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src import di
from src.data.logoscoffee.exceptions import InvalidToken, DatabaseError, UnknownError
from src.presentation.resources import strings
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.handlers.utils import get_token, invalid_token_error, unknown_error
from src.presentation.bots.client_bot.states import MainStates

router = Router()
client_service = di.container.client_service()


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
