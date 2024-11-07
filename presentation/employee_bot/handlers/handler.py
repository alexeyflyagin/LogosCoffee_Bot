from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.services.employee_service import employee_service as service
from data.services.exceptions import *
from presentation import strings
from presentation.employee_bot.constants import *
from presentation.employee_bot.states import *
from presentation.strings_builder import random_str

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    token = command.args
    if token is None:
        await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED)
        return
    try:
        await service.log_in(token)
        await state.set_data({TOKEN: token})
        await state.set_state(MainStates.Main)
        await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL))
    except InvalidToken:
        await msg.answer(strings.GENERAL.LOGIN.INVALID_TOKEN)
    except (DatabaseError, UnknownError):
        await msg.answer(random_str(strings.ERRORS.UNKNOWN))