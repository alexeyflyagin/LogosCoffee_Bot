from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.interfaces.event_service import EventService
from src.presentation.resources import strings
from src.presentation.bots.employee_bot.constants import *
from src.presentation.bots.employee_bot.states import *
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
employee_service: EmployeeService
event_service: EventService

@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    key = command.args
    if key is None:
        await msg.answer(strings.GENERAL.LOGIN.KEY_WAS_NOT_ENTERED)
        return
    try:
        account = await employee_service.login(key)
        await state.set_data({ACCOUNT_ID: account.id})
        await state.set_state(MainStates.Main)
        await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL))
    except InvalidKeyError:
        await  msg.answer(strings.GENERAL.LOGIN.INVALID_KEY)
    except (DatabaseError, UnknownError):
        await msg.answer(random_str(strings.ERRORS.UNKNOWN))