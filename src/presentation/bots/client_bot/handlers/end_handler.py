from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ErrorEvent

from src.data.logoscoffee.exceptions import InvalidTokenError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.loggers import bot_logger
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.handlers.utils import invalid_token_error, unknown_error, \
    unknown_error_for_callback
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.resources import strings

router = Router()
client_service: ClientService


@router.message(MainStates.Main)
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)


@router.error()
async def error_handler(event: ErrorEvent, state: FSMContext):
    if isinstance(event.exception, InvalidTokenError):
        bot_logger.debug(event.exception)
        if event.update.message:
            await invalid_token_error(event.update.message, state)
        elif event.update.callback_query:
            await invalid_token_error(event.update.callback_query.message, state)
            await event.update.callback_query.answer()
    else:
        bot_logger.exception(event.exception)
        if event.update.message:
            await unknown_error(event.update.message, state)
        elif event.update.callback_query:
            await unknown_error_for_callback(event.update.callback_query, state)
