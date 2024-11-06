from aiogram.filters import Command

from presentation import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from presentation.client_bot import keyboards, commands
from presentation.client_bot.handlers.utils import reset_state
from presentation.client_bot.states import *

router = Router()

@router.message(State(None))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(strings.CLIENT_URLS)
    await msg.answer(strings.CLIENT_AUTHORIZE_STATE1_MSG, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
    await state.set_state(LoginStates.PressButton)


@router.message(EnterReviewStates(), Command(commands.CANCEL_COMMAND))
async def cancel_handler(msg: Message, state: FSMContext):
    await reset_state(msg, state, strings.CANCEL_ACTION)

