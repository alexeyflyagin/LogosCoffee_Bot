from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.presentation.resources import strings
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.constants import ACCOUNT_ID
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.resources.strings_builder.strings_builder import random_str


async def reset_state(msg: Message, state: FSMContext, msg_text: str):
    await state.set_state(MainStates.Main)
    await msg.answer(msg_text, reply_markup=keyboards.MAIN_KEYBOARD)

async def unknown_error(msg: Message, state: FSMContext):
    await msg.answer(random_str(strings.ERRORS.UNKNOWN))
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)


async def get_account_id(state: FSMContext) -> int | None:
    data = await state.get_data()
    return data.get(ACCOUNT_ID, None)




