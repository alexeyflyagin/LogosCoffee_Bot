from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.services.admin_service import admin_service as service
from data.services.exceptions import InvalidToken, DatabaseError, UnknownError
from presentation import strings
from presentation.admin_bot.states import *

router = Router()

TOKEN = "token"

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    token = command.args
    if token is None:
        await msg.answer(strings.TOKEN_WAS_NOT_ENTERED)
        return
    try:
        await service.log_in(token)
        await state.set_data({TOKEN: token})
        await state.set_state(MainStates.Main)
        await msg.answer(strings.LOG_IN__SUCCESSFUL)
    except InvalidToken:
        await msg.answer(strings.INVALID_TOKEN)
    except (DatabaseError, UnknownError):
        await msg.answer(strings.UNKNOWN_ERROR)
