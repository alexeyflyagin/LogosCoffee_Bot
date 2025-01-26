from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.interfaces.admin_menu_service import AdminMenuService
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.loggers import bot_logger as logger
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers.utils import get_token, reset_state
from src.presentation.bots.admin_bot.states import MainStates, ChangeMenu
from src.presentation.bots.views.admin.models.menu import MenuViewData
from src.presentation.checks.checks import check_content_type
from src.presentation.checks.exceptions import ContentTypeError
from src.presentation.resources import strings

router = Router(name=__name__)
admin_service: AdminService
menu_service: AdminMenuService


@router.message(MainStates(), F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    await admin_service.validate_token(token)
    menu = await menu_service.get_menu()
    await MenuViewData.from_entity(menu).view().answer_view(msg)


@router.callback_query(F.data == constants.CHANGE_MENU_CD)
async def change_menu_callback(callback: CallbackQuery, state: FSMContext):
    token = await get_token(state)
    await admin_service.validate_token(token)
    await state.set_state(ChangeMenu.TextContent)
    await callback.message.answer(text=strings.ADMIN.CHANGE_MENU.ENTER_CONTENT, parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(MainStates(), F.text == strings.BTN.CHANGE_MENU)
async def change_menu_handler(msg: Message, state: FSMContext):
    token = await get_token(state)
    await admin_service.validate_token(token)
    await state.set_state(ChangeMenu.TextContent)
    await msg.answer(text=strings.ADMIN.CHANGE_MENU.ENTER_CONTENT, parse_mode=ParseMode.MARKDOWN,
                     reply_markup=ReplyKeyboardRemove())


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
