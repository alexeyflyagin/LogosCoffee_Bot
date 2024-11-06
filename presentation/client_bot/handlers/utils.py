from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from presentation import strings
from presentation.client_bot import keyboards
from presentation.client_bot.constants import TOKEN
from presentation.client_bot.states import MainStates, LoginStates


async def invalid_token_error(msg: Message, state: FSMContext):
    await state.set_state(LoginStates.PressButton)
    await state.set_data({})
    await msg.answer(strings.CLIENT_URLS)
    await msg.answer(strings.CLIENT_AUTHORIZE_STATE1_MSG, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)

async def reset_state(msg: Message, state: FSMContext, msg_text: str):
    await state.set_state(MainStates.Main)
    await msg.answer(msg_text, reply_markup=keyboards.MAIN_KEYBOARD)

async def get_token(state: FSMContext) -> str | None:
    data = await state.get_data()
    return data.get(TOKEN, None)
