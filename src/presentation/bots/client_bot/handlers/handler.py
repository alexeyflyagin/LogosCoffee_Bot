from aiogram.filters import Command

from src.presentation.resources import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.presentation.bots.client_bot import keyboards, commands
from src.presentation.bots.client_bot.handlers.utils import reset_state
from src.presentation.bots.client_bot.states import *

router = Router()

@router.message(State(None))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(strings.CLIENT.LINKS)
    await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
    await state.set_state(LoginStates.PressButton)


@router.message(EnterReviewStates(), Command(commands.CANCEL_COMMAND))
async def cancel_handler(msg: Message, state: FSMContext):
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)

