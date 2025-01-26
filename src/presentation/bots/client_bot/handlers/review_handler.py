from aiogram import F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.data.logoscoffee.exceptions import CooldownError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.bots.client_bot.handlers.utils import reset_state, get_token
from src.presentation.bots.client_bot.states import *
from src.presentation.checks.checks import check_content_type, ContentTypeError
from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str

router = Router()
client_service: ClientService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_REVIEW)
async def make_review_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    is_allowed = await client_service.can_submit_review(token)
    if not is_allowed:
        await msg.answer(random_str(strings.CLIENT.REVIEW.COOLDOWN_ERROR))
        return
    await msg.answer(strings.CLIENT.REVIEW.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(EnterReviewStates.EnterText)


@router.message(EnterReviewStates.EnterText)
async def make_review__content__handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        check_content_type(msg, ContentType.TEXT)
        await client_service.submit_review(token, msg.text)
        await reset_state(msg, state, random_str(strings.CLIENT.REVIEW.SUCCESSFUL))
    except ContentTypeError as e:
        await msg.answer(e.msg)
    except CooldownError:
        await msg.answer(random_str(strings.CLIENT.REVIEW.COOLDOWN_ERROR))
        await reset_state(msg, state, msg_text=strings.GENERAL.SELECT_ACTION)
