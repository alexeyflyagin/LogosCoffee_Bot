from aiogram.enums import ContentType

from data.services.client_service import client_service as service
from data.services.exceptions import DatabaseError, UnknownError
from presentation import strings
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from presentation.client_bot import keyboards
from presentation.client_bot.states import *
from presentation.client_bot.constants import TOKEN

router = Router()

@router.message(State(None), lambda x: x.content_type == ContentType.CONTACT)
async def contact_handler(msg: Message, state: FSMContext):
    if msg.contact.user_id != msg.from_user.id:
        await msg.answer(strings.CLIENT_AUTHORIZE_STATE1_MSG, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
        return
    try:
        log_in_data = await service.log_in(msg.contact.phone_number)
        await state.set_data({TOKEN: log_in_data.token})
        await state.set_state(MainStates.Main)
        await msg.answer("МОЛОДЕЦ", reply_markup=ReplyKeyboardRemove())
    except (DatabaseError, UnknownError):
        await msg.answer(strings.UNKNOWN_ERROR)


@router.message(State(None))
async def start_handler(msg: Message):
    await msg.answer(strings.CLIENT_AUTHORIZE_STATE1_MSG, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
