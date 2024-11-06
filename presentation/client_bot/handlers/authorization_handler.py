from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.services.exceptions import UnknownError, DatabaseError
from presentation import strings
from data.services.client_service import client_service as service
from presentation.client_bot import keyboards
from presentation.client_bot.constants import TOKEN
from presentation.client_bot.states import LoginStates, MainStates

router = Router()

async def send_authorization_request_msg(msg: Message):
    await msg.answer(strings.CLIENT_AUTHORIZE_STATE1_MSG, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)


@router.message(LoginStates.PressButton, lambda x: x.content_type == ContentType.CONTACT)
async def contact_handler(msg: Message, state: FSMContext):
    if msg.contact.user_id != msg.from_user.id:
        await send_authorization_request_msg(msg)
        return
    try:
        log_in_data = await service.log_in(msg.contact.phone_number)
        await state.set_data({TOKEN: log_in_data.token})
        await state.set_state(MainStates.Main)
        await msg.answer(strings.CLIENT__LOG_IN__SUCCESSFUL, reply_markup=keyboards.MAIN_KEYBOARD)
    except (DatabaseError, UnknownError):
        await msg.answer(strings.UNKNOWN_ERROR)

@router.message(LoginStates.PressButton)
async def start_authorize_handler(msg: Message):
    await send_authorization_request_msg(msg)