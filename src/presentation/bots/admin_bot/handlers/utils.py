from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from src.presentation.bots.admin_bot import constants, keyboards
from src.presentation.bots.admin_bot.states import MainStates
from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str


async def reset_state(msg: Message, state: FSMContext, msg_text: str):
    await state.set_state(MainStates.Main)
    await msg.answer(msg_text, reply_markup=keyboards.MAIN_KEYBOARD)


async def unknown_error(msg: Message, state: FSMContext):
    await msg.answer(random_str(strings.ERRORS.UNKNOWN))
    await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)


async def invalid_token_error(msg: Message, state: FSMContext):
    await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)
    await state.set_data({})


async def unknown_error_for_callback(callback: CallbackQuery, state: FSMContext):
    # Probably `state` will be useful in the future
    await callback.answer(random_str(strings.ERRORS.UNKNOWN))


async def get_token(state: FSMContext) -> str | None:
    data = await state.get_data()
    return data.get(constants.TOKEN, None)
