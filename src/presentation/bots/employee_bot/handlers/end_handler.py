from aiogram import Router
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from src.presentation.bots.employee_bot.states import MainStates
from src.presentation.resources import strings

router = Router()


@router.message(State(None))
async def other_handler(msg: Message):
    await msg.answer(strings.GENERAL.LOGIN.TOKEN_WAS_NOT_ENTERED, reply_markup=ReplyKeyboardRemove())


@router.message(MainStates())
async def other_handler(msg: Message):
    await msg.delete()
