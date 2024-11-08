from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src import di
from src.data.logoscoffee.services import employee_service_impl as service
from src.data.logoscoffee.exceptions import *
from src.presentation.resources import strings
from src.presentation.bots.employee_bot.constants import *
from src.presentation.bots.employee_bot.states import *
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
employee_service = di.container.employee_service()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    token = command.args
    if token is None:
        await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED)
        return
    try:
        await employee_service.login(token)
        await state.set_data({TOKEN: token})
        await state.set_state(MainStates.Main)
        await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL))
    except InvalidToken:
        await msg.answer(strings.GENERAL.LOGIN.INVALID_TOKEN)
    except (DatabaseError, UnknownError):
        await msg.answer(random_str(strings.ERRORS.UNKNOWN))