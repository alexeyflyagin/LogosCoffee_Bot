from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, OfferDoesNotExist, CooldownError
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers.utils import unknown_error, reset_state, unknown_error_for_callback, \
    get_account_id
from src.presentation.bots.admin_bot.keyboards import OfferCD, offer_markup
from src.presentation.bots.admin_bot.states import MainStates, MakePromotionalOffer
from src.presentation.bots.confirmation_markup import ConfirmationCD, confirmation_markup
from src.presentation.bots.types import FileAddress
from src.presentation.bots.utils import send_or_update_msg, get_datetime_str, \
    send_offer, get_date_last_offer_distributing_str
from src.presentation.checks import checks
from src.presentation.checks.exceptions import ContentTypeException
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_PROMOTIONAL_OFFER)
async def create_offer_handler(msg: Message, state: FSMContext):
    await state.set_state(MakePromotionalOffer.Content)
    await msg.answer(strings.ADMIN.MAKE_OFFER.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())


@router.message(MakePromotionalOffer.Content)
async def create_offer__content__handler(msg: Message, state: FSMContext):
    try:
        checks.check_content_type(msg, ContentType.TEXT, ContentType.PHOTO)
        text = msg.text
        preview_photo = None
        if msg.content_type == ContentType.PHOTO:
            text = msg.caption
            preview_photo = FileAddress(msg.bot.token, msg.photo[-1].file_id).address
        res = await admin_service.create_promotional_offer(text, preview_photo)
        await show_offer_management(msg, res.id)
        await reset_state(msg, state, strings.GENERAL.SELECT_ACTION)
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.callback_query(OfferCD.filter())
async def offer_callback(callback: CallbackQuery, state: FSMContext):
    data = OfferCD.unpack(callback.data)
    try:
        offer = await admin_service.get_promotional_offer(data.offer_id)
        if data.action == data.Action.PUBLISH:
            await callback.message.edit_text(
                text=strings.ADMIN.OFFER.PUBLISH.WARNING.format(offer_id=data.offer_id),
                reply_markup=confirmation_markup(tag=constants.TAG__DISTRIBUTE_OFFER, p_arg=data.offer_id),
            )
        elif data.action == data.Action.DELETE:
            await callback.message.edit_text(
                text=strings.ADMIN.OFFER.DELETE.WARNING.format(offer_id=data.offer_id),
                reply_markup=confirmation_markup(tag=constants.TAG__DELETE_OFFER, p_arg=data.offer_id),
            )
        elif data.action == data.Action.SHOW:
            await send_offer(callback.bot, callback.message.chat.id, offer)
            await callback.answer()
    except OfferDoesNotExist:
        await callback.answer(strings.ADMIN.OFFER.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(ConfirmationCD.filter(F.tag == constants.TAG__DISTRIBUTE_OFFER))
async def distribute_offer_callback(callback: CallbackQuery, state: FSMContext):
    account_id = await get_account_id(state)
    data = ConfirmationCD.unpack(callback.data)
    offer_id = int(data.p_arg)
    try:
        if data.action == data.Action.CONFIRM:
            await admin_service.distribute_promotional_offer(account_id, offer_id)
            await callback.answer(strings.ADMIN.OFFER.PUBLISH.SUCCESSFUL)
            await show_offer_management(callback.message, offer_id, is_update=True)
        elif data.action == data.Action.CANCEL:
            await show_offer_management(callback.message, offer_id, is_update=True)
    except CooldownError:
        await callback.answer(strings.ADMIN.OFFER.PUBLISH.COOLDOWN_ERROR)
    except OfferDoesNotExist:
        await callback.answer(strings.ADMIN.OFFER.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


@router.callback_query(ConfirmationCD.filter(F.tag == constants.TAG__DELETE_OFFER))
async def delete_offer_callback(callback: CallbackQuery, state: FSMContext):
    data = ConfirmationCD.unpack(callback.data)
    offer_id = int(data.p_arg)
    try:
        if data.action == data.Action.CONFIRM:
            await admin_service.delete_promotional_offer(offer_id)
            await callback.answer(strings.ADMIN.OFFER.DELETE.SUCCESSFUL)
            await callback.message.delete()
        elif data.action == data.Action.CANCEL:
            await show_offer_management(callback.message, offer_id, is_update=True)
    except OfferDoesNotExist:
        await callback.answer(strings.ADMIN.OFFER.DOES_NOT_EXIST)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


async def show_offer_management(msg: Message, offer_id: int, is_update: bool = False):
    text = strings.ADMIN.OFFER.DOES_NOT_EXIST
    try:
        offer = await admin_service.get_promotional_offer(offer_id)
        markup = offer_markup(offer_id)
        text = strings.ADMIN.OFFER.MAIN.format(
            offer_id=offer.id, date_last_distribute=get_date_last_offer_distributing_str(offer),
            date_create=get_datetime_str(offer.date_create)
        )
        await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=markup)
    except OfferDoesNotExist:
        await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=None)
