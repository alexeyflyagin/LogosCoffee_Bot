from aiogram.filters import Command

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AlreadySubscribedError
from src.data.logoscoffee.interfaces.event_service import EventService
from src.presentation.bots.admin_bot.handlers.utils import unknown_error
from src.presentation.resources import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.presentation.bots.client_bot import keyboards, commands, constants
from src.presentation.bots.client_bot.handlers.utils import reset_state
from src.presentation.bots.client_bot.states import *

router = Router()
event_service: EventService


@router.message(State(None))
async def start_handler(msg: Message, state: FSMContext):
    try:
        await msg.answer(strings.CLIENT.LINKS)
        await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
        await state.set_state(AuthorizationStates.PressButton)
        await event_service.subscribe(constants.EVENT__NEW_ANNOUNCEMENT, msg.chat.id)
    except AlreadySubscribedError:
        pass
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.message(EnterReviewStates(), Command(commands.CANCEL_COMMAND))
async def cancel_handler(msg: Message, state: FSMContext):
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)
