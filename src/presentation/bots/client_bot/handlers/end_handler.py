from aiogram import Router
from aiogram.types import Message

from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.resources import strings
from src.presentation.bots.client_bot import keyboards
from src.presentation.bots.client_bot.states import MainStates

router = Router()
client_service: ClientService


@router.message(MainStates.Main)
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)
