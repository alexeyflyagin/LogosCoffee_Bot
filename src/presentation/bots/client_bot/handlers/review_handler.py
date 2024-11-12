from aiogram.enums import ContentType

from aiogram import F

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, EmptyTextError, CooldownError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.resources import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.presentation.checks.checks import check_content_type, ContentTypeException
from src.presentation.bots.client_bot.handlers.utils import reset_state, unknown_error, \
    get_account_id
from src.presentation.bots.client_bot.states import *
from src.presentation.resources.strings_builder.strings_builder import random_str


router = Router()
client_service: ClientService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_REVIEW)
async def start_make_review_handler(msg: Message, state: FSMContext):
    account_id = await get_account_id(state)
    try:
        await client_service.can_create_review(account_id)
        await msg.answer(strings.CLIENT.REVIEW.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(EnterReviewStates.EnterText)
    except CooldownError:
        await msg.answer(random_str(strings.CLIENT.REVIEW.COOLDOWN_ERROR))
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.message(EnterReviewStates.EnterText)
async def content_review_handler(msg: Message, state: FSMContext):
    account_id = await get_account_id(state)
    try:
        check_content_type(msg, ContentType.TEXT)
        await client_service.create_review(account_id, msg.text)
        await reset_state(msg, state, random_str(strings.CLIENT.REVIEW.SUCCESSFUL))
    except CooldownError:
        await msg.answer(random_str(strings.CLIENT.REVIEW.COOLDOWN_ERROR))
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except (DatabaseError, UnknownError, EmptyTextError):
        await unknown_error(msg, state)