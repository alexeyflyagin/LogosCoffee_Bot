from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.exceptions import UnknownError, DatabaseError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.resources import strings
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.constants import ACCOUNT_ID
from src.presentation.bots.client_bot.handlers.utils import unknown_error
from src.presentation.bots.client_bot.states import LoginStates, MainStates
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
client_service: ClientService

async def send_authorization_request_msg(msg: Message):
    await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)


@router.message(LoginStates.PressButton, lambda x: x.content_type == ContentType.CONTACT)
async def contact_handler(msg: Message, state: FSMContext):
    if msg.contact.user_id != msg.from_user.id:
        await send_authorization_request_msg(msg)
        return
    try:
        account = await client_service.login(msg.contact.phone_number)
        await state.set_data({ACCOUNT_ID: account.id})
        await state.set_state(MainStates.Main)
        await msg.answer(random_str(strings.CLIENT.AUTHORIZATION.SUCCESSFUL), reply_markup=keyboards.MAIN_KEYBOARD)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.message(LoginStates.PressButton)
async def start_authorize_handler(msg: Message):
    await send_authorization_request_msg(msg)