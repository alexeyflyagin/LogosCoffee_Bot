from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from presentation import strings
from presentation.client_bot import keyboards
from presentation.client_bot.constants import TOKEN
from presentation.client_bot.states import MainStates, LoginStates
from presentation.strings_builder import random_str


async def reset_state(msg: Message, state: FSMContext, msg_text: str):
    await state.set_state(MainStates.Main)
    await msg.answer(msg_text, reply_markup=keyboards.MAIN_KEYBOARD)

async def invalid_token_error(msg: Message, state: FSMContext):
    await state.set_state(LoginStates.PressButton)
    await state.set_data({})
    await msg.answer(strings.CLIENT.LINKS)
    await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)

async def unknown_error(msg: Message, state: FSMContext):
    await msg.answer(random_str(strings.ERRORS.UNKNOWN))
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)


async def get_token(state: FSMContext) -> str | None:
    data = await state.get_data()
    return data.get(TOKEN, None)




