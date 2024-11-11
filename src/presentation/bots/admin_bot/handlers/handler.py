from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.exceptions import InvalidToken, DatabaseError, UnknownError, AlreadySubscribedError
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.data.logoscoffee.interfaces.event_service import EventService
from src.presentation.bots.admin_bot import constants, keyboards, commands
from src.presentation.bots.admin_bot.constants import TOKEN
from src.presentation.bots.admin_bot.handlers.utils import reset_state
from src.presentation.resources import strings
from src.presentation.bots.admin_bot.states import *
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
admin_service: AdminService
event_service: EventService

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext, command: CommandObject):
    token = command.args
    if token is None:
        await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED)
        return
    try:
        await admin_service.login(token)
        await state.set_data({TOKEN: token})
        await state.set_state(MainStates.Main)
        user_state_id = await event_service.get_user_state_id(msg.bot.id, msg.from_user.id, msg.chat.id)
        await event_service.subscribe(constants.EVENT__NEW_REVIEW, user_state_id)
        await msg.answer(random_str(strings.GENERAL.LOGIN.SUCCESSFUL), reply_markup=keyboards.MAIN_KEYBOARD)
    except AlreadySubscribedError:
        pass
    except InvalidToken:
        await msg.answer(strings.GENERAL.LOGIN.INVALID_TOKEN)
    except (DatabaseError, UnknownError):
        await msg.answer(random_str(strings.ERRORS.UNKNOWN))

@router.message(MakePromotionalOffer(), Command(commands.CANCEL_COMMAND))
async def cancel_handler(msg: Message, state: FSMContext):
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)
