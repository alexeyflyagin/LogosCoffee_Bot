from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AnnouncementNotFoundError, CooldownError, \
    InvalidTokenError
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot.constants import Tag
from src.presentation.bots.admin_bot.handlers.utils import unknown_error, reset_state, unknown_error_for_callback, \
    get_token, invalid_token_error
from src.presentation.bots.admin_bot.states import MainStates, MakeAnnouncement
from src.presentation.bots.middlewares.one_message_middleware import OneMessageMiddleware
from src.presentation.bots.types import FileAddress
from src.presentation.bots.utils import send_announcement
from src.presentation.bots.views.admin.callbacks.announcement import AnnouncementCD
from src.presentation.bots.views.admin.models.announcement import AnnouncementViewData
from src.presentation.bots.views.default.callbacks.confirmation import ConfirmationCD
from src.presentation.bots.views.default.models.confirmation import ConfirmationViewData
from src.presentation.checks import checks
from src.presentation.checks.exceptions import ContentTypeError, MessageContentCountError
from src.presentation.resources import strings

router = Router()
OneMessageMiddleware(router, one_message_states=[MakeAnnouncement.Content])
admin_service: AdminService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_ANNOUNCEMENT)
async def create_announcement_handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        is_allowed = await admin_service.can_create_or_distribute_announcement(token)
        if not is_allowed:
            await msg.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.COOLDOWN_ERROR)
            return
        await state.set_state(MakeAnnouncement.Content)
        await msg.answer(strings.ADMIN.MAKE_ANNOUNCEMENT.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())
    except InvalidTokenError:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.message(MakeAnnouncement.Content)
async def create_announcement__content__handler(msg: Message, state: FSMContext, msg_count: int):
    try:
        token = await get_token(state)
        checks.check_one_msg(msg_count)
        checks.check_content_type(msg, ContentType.TEXT, ContentType.PHOTO)
        text = msg.text
        preview_photo = None
        if msg.content_type == ContentType.PHOTO:
            text = msg.caption
            preview_photo = FileAddress(FileAddress.BotType.ADMIN_BOT, msg.photo[-1].file_id).address
        res = await admin_service.create_announcement(token, text, preview_photo)
        await AnnouncementViewData.from_entity(res).view().answer_view(msg)
        await reset_state(msg, state, strings.GENERAL.SELECT_ACTION)
    except (ContentTypeError, MessageContentCountError) as e:
        await msg.answer(e.msg)
    except CooldownError:
        await msg.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.COOLDOWN_ERROR)
        await reset_state(msg, state, strings.GENERAL.ACTION_CANCELED)
    except InvalidTokenError:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.callback_query(AnnouncementCD.filter())
async def announcement_callback(callback: CallbackQuery, state: FSMContext):
    data = AnnouncementCD.unpack(callback.data)
    try:
        token = await get_token(state)
        announcement = await admin_service.get_announcement_by_id(token, data.announcement_id)
        if data.action == data.Action.PUBLISH:
            await ConfirmationViewData(
                text=strings.ADMIN.ANNOUNCEMENT.PUBLISH.WARNING.format(announcement_id=data.announcement_id),
                tag=Tag.TAG__DISTRIBUTE_ANNOUNCEMENT,
                p_arg=data.announcement_id,
            ).view().edit_view(msg=callback.message)
        elif data.action == data.Action.SHOW:
            await send_announcement(callback.bot, callback.message.chat.id, announcement)
            await callback.answer()
    except AnnouncementNotFoundError:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST)
        await callback.message.edit_reply_markup(reply_markup=None)
    except InvalidTokenError:
        await invalid_token_error(callback.msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(ConfirmationCD.filter(F.tag == Tag.TAG__DISTRIBUTE_ANNOUNCEMENT))
async def distribute_announcement_callback(callback: CallbackQuery, state: FSMContext):
    try:
        data = ConfirmationCD.unpack(callback.data)
        announcement_id = data.p_arg
        token = await get_token(state)
        if data.action == data.Action.CONFIRM:
            await admin_service.distribute_announcement(token, announcement_id)
            await callback.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.TOAST_SUCCESSFUL)
            await callback.message.edit_text(text=strings.ADMIN.ANNOUNCEMENT.PUBLISH.SUCCESSFUL, reply_markup=None)
        elif data.action == data.Action.CANCEL:
            announcement = await admin_service.get_announcement_by_id(token, announcement_id)
            await AnnouncementViewData.from_entity(announcement).view().edit_view(callback.message)
    except CooldownError:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.PUBLISH.COOLDOWN_ERROR)
    except AnnouncementNotFoundError:
        await callback.answer(strings.ADMIN.ANNOUNCEMENT.DOES_NOT_EXIST)
        await callback.message.edit_reply_markup(reply_markup=None)
    except InvalidTokenError:
        await invalid_token_error(callback.msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)
