from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loguru import logger

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, InvalidTokenError
from src.data.logoscoffee.interfaces.admin_menu_service import AdminMenuService
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import keyboards, constants
from src.presentation.bots.admin_bot.handlers.utils import get_token, invalid_token_error, reset_state, \
    unknown_error_for_callback
from src.presentation.bots.admin_bot.handlers.utils import unknown_error
from src.presentation.bots.admin_bot.states import MainStates, ChangeMenu
from src.presentation.bots.utils import send_or_update_msg
from src.presentation.checks.checks import check_content_type
from src.presentation.checks.exceptions import ContentTypeError
from src.presentation.resources import strings

router = Router(name=__name__)
admin_service: AdminService
menu_service: AdminMenuService


@router.message(MainStates(), F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    await show_menu(msg, state)


@router.message(F.data == constants.CHANGE_MENU_CALLBACK_DATA)
async def change_menu_callback(callback: CallbackQuery, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        await state.set_state(ChangeMenu.TextContent)
        await callback.message.answer(text=strings.ADMIN.CHANGE_MENU.ENTER_CONTENT, parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=ReplyKeyboardRemove())
        await callback.answer()
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(callback.msg, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error_for_callback(callback, state)


@router.message(MainStates(), F.text == strings.BTN.CHANGE_MENU)
async def change_menu_handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        await state.set_state(ChangeMenu.TextContent)
        await msg.answer(text=strings.ADMIN.CHANGE_MENU.ENTER_CONTENT, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error(msg, state)


@router.message(ChangeMenu.TextContent)
async def change_menu__text_content__handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        check_content_type(msg, ContentType.TEXT)
        await menu_service.update_menu(token, text_content=msg.text)
        await reset_state(msg, state, msg_text=strings.ADMIN.CHANGE_MENU.SUCCESS)
    except ContentTypeError as e:
        logger.debug(e.log_msg)
        await msg.answer(e.msg)
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error(msg, state)


async def show_menu(msg: Message, state: FSMContext):
    try:
        menu = await menu_service.get_menu()
        text = menu.text_content or strings.ADMIN.EMPTY_MENU_CONTENT
        markup = None if menu.text_content else keyboards.EMPTY_MENU_IK
        await send_or_update_msg(msg, text=text, replay_markup=markup)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.exception(e)
        await unknown_error(msg, state)
