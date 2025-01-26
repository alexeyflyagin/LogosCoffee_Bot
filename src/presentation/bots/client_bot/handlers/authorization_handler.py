from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.constants import TOKEN
from src.presentation.bots.client_bot.states import AuthorizationStates, MainStates
from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
client_service: ClientService


async def send_authorization_request_msg(msg: Message):
    await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)


@router.message(AuthorizationStates.PressButton)
async def contact_handler(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.CONTACT or msg.contact.user_id != msg.from_user.id:
        await msg.answer(strings.CLIENT.AUTHORIZATION.PRESS_BTN, reply_markup=keyboards.AUTHORIZATION_KEYBOARD)
        return
    account = await client_service.authorization(msg.contact.phone_number)
    await state.set_data({TOKEN: account.token})
    await state.set_state(MainStates.Main)
    await msg.answer(random_str(strings.CLIENT.AUTHORIZATION.SUCCESSFUL), reply_markup=keyboards.MAIN_KEYBOARD)
