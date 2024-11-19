from loguru import logger

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AlreadySubscribedError, InvalidKey
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.data.logoscoffee.interfaces.event_service import EventService
from src.presentation.bots.admin_bot import constants, keyboards, commands
from src.presentation.bots.admin_bot.constants import ACCOUNT_ID
from src.presentation.bots.admin_bot.handlers.utils import reset_state, unknown_error
from src.presentation.resources import strings
from src.presentation.bots.admin_bot.states import *
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
admin_service: AdminService
event_service: EventService

@router.message(State(None), CommandStart())
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    key = command.args
    if key is None:
        await msg.answer(strings.GENERAL.LOGIN.KEY_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())
        return
    try:
        account = await admin_service.login(key)
        await state.set_data({ACCOUNT_ID: account.id})
        await state.set_state(MainStates.Main)
        await event_service.subscribe(constants.EVENT__NEW_REVIEW, msg.chat.id)
        await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL), reply_markup=keyboards.MAIN_KEYBOARD)
        await msg.delete()
    except AlreadySubscribedError:
        pass
    except InvalidKey:
        await msg.answer(text=strings.GENERAL.LOGIN.INVALID_KEY, reply_markup=ReplyKeyboardRemove())
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.message(MakeAnnouncement(), Command(commands.CANCEL_COMMAND))
async def cancel_handler(msg: Message, state: FSMContext):
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)
