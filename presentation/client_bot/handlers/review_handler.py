from aiogram.enums import ContentType

from aiogram import F

from data.services.client_service import client_service as service
from data.services.exceptions import DatabaseError, UnknownError, EmptyTextError, CooldownError, InvalidToken
from presentation import strings
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from presentation.checks import check_content_type, ContentTypeException
from presentation.client_bot import command_strings
from presentation.client_bot.handlers.utils import reset_state, get_token, invalid_token_error
from presentation.client_bot.states import *

router = Router()


@router.message(MainStates.Main, F.text == command_strings.MAKE_REVIEW)
async def start_make_review_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        await service.can_make_review(token)
        await msg.answer(strings.CLIENT__REVIEW__ENTER_TEXT, reply_markup=ReplyKeyboardRemove())
        await state.set_state(EnterReviewStates.EnterText)
    except CooldownError:
        await msg.answer(strings.CLIENT__REVIEW__COOLDOWN_ERROR)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await msg.answer(strings.UNKNOWN_ERROR)

@router.message(EnterReviewStates.EnterText)
async def content_review_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    try:
        check_content_type(msg, ContentType.TEXT)
        await service.make_review(token, msg.text)
        await reset_state(msg, state, strings.CLIENT__REVIEW__ANSWER)
    except CooldownError:
        await msg.answer(strings.CLIENT__REVIEW__COOLDOWN_ERROR)
    except EmptyTextError:
        await msg.answer(strings.CLIENT__REVIEW__EMPTY_TEXT_ERROR)
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await msg.answer(strings.UNKNOWN_ERROR)