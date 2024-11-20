from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AnnouncementDoesNotExist, CooldownError
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers.utils import unknown_error, reset_state, unknown_error_for_callback, \
    get_account_id
from src.presentation.bots.admin_bot.keyboards import AnnouncementCD, announcement_markup
from src.presentation.bots.admin_bot.states import MainStates, MakeAnnouncement
from src.presentation.bots.confirmation_markup import ConfirmationCD, confirmation_markup
from src.presentation.bots.constants import CALLBACK_DATA__LIST_MENU
from src.presentation.bots.types import FileAddress
from src.presentation.bots.utils import send_or_update_msg, get_datetime_str, get_date_last_announcement_distributing_str, \
    send_announcement
from src.presentation.checks import checks
from src.presentation.checks.exceptions import ContentTypeException
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_ANNOUNCEMENT)
async def create_announcement_handler(msg: Message, state: FSMContext):
    await state.set_state(MakeAnnouncement.Content)
    await msg.answer(strings.ADMIN.MAKE_ANNOUNCEMENT.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())


@router.message(MakeAnnouncement.Content)
async def create_announcement__content__handler(msg: Message, state: FSMContext):
    try:
        checks.check_content_type(msg, ContentType.TEXT, ContentType.PHOTO)
        text = msg.text
        preview_photo = None
        if msg.content_type == ContentType.PHOTO:
            text = msg.caption
            preview_photo = FileAddress(FileAddress.BotType.ADMIN_BOT, msg.photo[-1].file_id).address
        res = await admin_service.create_announcement(text, preview_photo)
        await show_announcement_management(msg, res.id)
        await reset_state(msg, state, strings.GENERAL.SELECT_ACTION)
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.callback_query(AnnouncementCD.filter())
async def announcement_callback(callback: CallbackQuery, state: FSMContext):
    data = AnnouncementCD.unpack(callback.data)
    try:
        announcement = await admin_service.get_announcement(data.announcement_id)
        if data.action == data.Action.PUBLISH:
            await callback.message.edit_text(
                text=strings.ADMIN.ANNOUNCEMENT.PUBLISH.WARNING.format(announcement_id=data.announcement_id),
                reply_markup=confirmation_markup(tag=constants.TAG__DISTRIBUTE_ANNOUNCEMENT, p_arg=data.announcement_id),
            )
        elif data.action == data.Action.DELETE:
            await callback.message.edit_text(
                text=strings.ADMIN.ANNOUNCEMENT.DELETE.WARNING.format(announcement_id=data.announcement_id),
                reply_markup=confirmation_markup(tag=constants.TAG__DELETE_ANNOUNCEMENT, p_arg=data.announcement_id),
            )
        elif data.action == data.Action.SHOW:
            await send_announcement(callback.bot, callback.message.chat.id, announcement)
            await callback.answer()
    except AnnouncementDoesNotExist:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(ConfirmationCD.filter(F.tag == constants.TAG__DISTRIBUTE_ANNOUNCEMENT))
async def distribute_announcement_callback(callback: CallbackQuery, state: FSMContext):
    account_id = await get_account_id(state)
    data = ConfirmationCD.unpack(callback.data)
    announcement_id = int(data.p_arg)
    try:
        if data.action == data.Action.CONFIRM:
            await admin_service.distribute_announcement(account_id, announcement_id)
            await callback.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.SUCCESSFUL)
            await show_announcement_management(callback.message, announcement_id, is_update=True)
        elif data.action == data.Action.CANCEL:
            await show_announcement_management(callback.message, announcement_id, is_update=True)
    except CooldownError:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.COOLDOWN_ERROR)
    except AnnouncementDoesNotExist:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(ConfirmationCD.filter(F.tag == constants.TAG__DELETE_ANNOUNCEMENT))
async def delete_announcement_callback(callback: CallbackQuery, state: FSMContext):
    data = ConfirmationCD.unpack(callback.data)
    announcement_id = int(data.p_arg)
    try:
        if data.action == data.Action.CONFIRM:
            await admin_service.delete_announcement(announcement_id)
            await callback.answer(strings.ADMIN.ANNOUNCEMENT.DELETE.SUCCESSFUL)
            await callback.message.delete()
        elif data.action == data.Action.CANCEL:
            await show_announcement_management(callback.message, announcement_id, is_update=True)
    except AnnouncementDoesNotExist:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(MainStates.Main, F.data == CALLBACK_DATA__LIST_MENU)
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.BUTTON_MENU_FOR_CLIENT)
    except (DatabaseError, UnknownError):
        await unknown_error(callback.message, state)


async def show_announcement_management(msg: Message, announcement_id: int, is_update: bool = False):
    text = strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST
    try:
        announcement = await admin_service.get_announcement(announcement_id)
        markup = announcement_markup(announcement_id)
        text = strings.ADMIN.ANNOUNCEMENT.MAIN.format(
            announcement_id=announcement.id, date_last_distribute=get_date_last_announcement_distributing_str(announcement),
            date_create=get_datetime_str(announcement.date_create)
        )
        await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=markup)
    except AnnouncementDoesNotExist:
        await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=None)
