from aiogram import Router, F
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.exceptions import AlreadySubscribedError
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.interfaces.event_service import EventService
from src.presentation.bots.constants import CALLBACK_DATA__LIST_MENU
from src.presentation.bots.employee_bot import constants
from src.presentation.bots.employee_bot.constants import TOKEN
from src.presentation.bots.employee_bot.states import MainStates
from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
employee_service: EmployeeService
event_service: EventService


@router.message(State(None), CommandStart())
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    token = command.args
    if not token:
        await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())
        return
    account = await employee_service.authorization(token)
    await state.set_data({TOKEN: account.token})
    await state.set_state(MainStates.Main)
    try:
        await event_service.subscribe(constants.EVENT__NEW_ORDER, msg.chat.id)
    except AlreadySubscribedError:
        pass
    await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL))
    await msg.delete()


@router.callback_query(MainStates.Main, F.data == CALLBACK_DATA__LIST_MENU)
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.ADMIN.ANNOUNCEMENT.BUTTON_MENU_FOR_CLIENT)
