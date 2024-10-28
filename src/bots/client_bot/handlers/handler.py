from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(CommandStart)
async def start_handler(msg: Message, state: FSMContext):
    await msg.reply(msg.text)
