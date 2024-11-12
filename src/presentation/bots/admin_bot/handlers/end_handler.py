from aiogram import Router
from aiogram.types import Message

from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import keyboards
from src.presentation.bots.admin_bot.states import MainStates
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(MainStates.Main)
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)
