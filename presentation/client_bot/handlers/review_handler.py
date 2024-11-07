from aiogram.enums import ContentType

from aiogram import F

from data.services.client_service import client_service as service
from data.services.exceptions import DatabaseError, UnknownError, EmptyTextError, CooldownError, InvalidToken
from presentation import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from presentation.checks import check_content_type, ContentTypeException
from presentation.client_bot.handlers.utils import reset_state, get_token, invalid_token_error, unknown_error
from presentation.client_bot.states import *
from presentation.strings_builder import random_str

router = Router()


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_REVIEW)
async def start_make_review_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        await service.can_make_review(token)
        await msg.answer(strings.CLIENT.REVIEW.ENTER_REVIEW_CONTENT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(EnterReviewStates.EnterText)
    except CooldownError:
        await msg.answer(random_str(strings.CLIENT.REVIEW.REVIEW__COOLDOWN_ERROR))
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.message(EnterReviewStates.EnterText)
async def content_review_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        check_content_type(msg, ContentType.TEXT)
        await service.make_review(token, msg.text)
        await reset_state(msg, state, random_str(strings.CLIENT.REVIEW.SUCCESSFUL))
    except CooldownError:
        await msg.answer(random_str(strings.CLIENT.REVIEW.REVIEW__COOLDOWN_ERROR))
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError, EmptyTextError):
        await unknown_error(msg, state)