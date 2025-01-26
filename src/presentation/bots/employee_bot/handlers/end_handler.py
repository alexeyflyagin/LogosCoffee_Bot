from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, ErrorEvent

from src.data.logoscoffee.exceptions import InvalidTokenError
from src.loggers import bot_logger
from src.presentation.bots.employee_bot.handlers.utils import invalid_token_error, unknown_error, \
    unknown_error_for_callback
from src.presentation.bots.employee_bot.states import MainStates
from src.presentation.resources import strings

router = Router()


@router.message(State(None))
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())


@router.message(MainStates())
async def other_handler(msg: Message):
    await msg.delete()


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
