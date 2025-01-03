from aiogram import Router
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import keyboards
from src.presentation.bots.admin_bot.states import MainStates
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(State(None))
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())


@router.message(MainStates.Main)
async def other_for_authorized_client_handler(msg: Message):
    await msg.answer(strings.GENERAL.SELECT_ACTION, reply_markup=keyboards.MAIN_KEYBOARD)
