from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from src.states import *
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.set_state(None)
    await msg.answer("Started")