
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.data.logoscoffee.exceptions import InvalidToken, DatabaseError, UnknownError, PromotionalOfferDoesNotExist
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers.end_handler import admin_service
from src.presentation.bots.admin_bot.handlers.utils import get_token, invalid_token_error, unknown_error, \
    generate_file_url, reset_state
from src.presentation.bots.admin_bot.states import MainStates, MakePromotionalOffer
from src.presentation.checks import checks
from src.presentation.checks.exceptions import ContentTypeException
from src.presentation.resources import strings

router = Router()
admin_service: AdminService

class PromotionalOfferCD(CallbackData, prefix=constants.CD_PREFIX__PROMOTIONAL_OFFER):
    token: str
    offer_id: int
    action: int

    class Action:
        PUBLISH = 0
        DELETE = 1


def promotional_offer_markup(token: str, offer_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    publish_data = PromotionalOfferCD(token=token, offer_id=offer_id, action=PromotionalOfferCD.Action.PUBLISH).pack()
    delete_data = PromotionalOfferCD(token=token, offer_id=offer_id, action=PromotionalOfferCD.Action.DELETE).pack()
    ikb.add(InlineKeyboardButton(text=strings.BTN.PUBLISH, callback_data=publish_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.DELETE, callback_data=delete_data))
    return ikb.as_markup()


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_PROMOTIONAL_OFFER)
async def write_promotional_offer_handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        await state.set_state(MakePromotionalOffer.Content)
        await msg.answer(strings.ADMIN.MAKE_PROMOTIONAL_OFFER.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.message(MakePromotionalOffer.Content)
async def make_promotional_offer__content__handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        checks.check_content_type(msg, ContentType.TEXT, ContentType.PHOTO)
        text = None
        preview_photo_url = None
        if msg.content_type == ContentType.PHOTO:
            text = msg.caption
            file = await msg.bot.get_file(msg.photo[-1].file_id)
            preview_photo_url = generate_file_url(msg.bot.token, file.file_path)
        else:
            text = msg.text
        res = await admin_service.make_promotional_offer(token, text, preview_photo_url)
        await show_promotional_offer(token, msg, res.id)
        await reset_state(msg, state, strings.GENERAL.SELECT_ACTION)
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except InvalidToken:
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.callback_query(PromotionalOfferCD.filter())
async def promotional_offer_callback(callback: CallbackQuery, state: FSMContext):
    try:
        token = await get_token(state)
        await admin_service.validate_token(token)
        data = PromotionalOfferCD.unpack(callback.data)
        if data.action == data.Action.PUBLISH:
            await admin_service.start_promotional_offer(data.token, data.offer_id)
            await callback.message.edit_text(callback.message.text + "\n\n(опубликованно)", reply_markup=None)
            await callback.answer("успешно опубликовано") # TODO поменять надписи
        elif data.action == data.Action.DELETE:
            await admin_service.delete_promotional_offer(token, data.offer_id)
            await callback.answer("успешно удаленно")
    except PromotionalOfferDoesNotExist:
        await callback.answer("Акция не найдена.")
    except InvalidToken:
        await invalid_token_error(callback.message, state)
    except (DatabaseError, UnknownError):
        await unknown_error(callback.message, state)


async def show_promotional_offer(token: str | None, msg: Message, offer_id: int):
    try:
        offer = await admin_service.get_promotional_offer(token, offer_id)
        markup = promotional_offer_markup(token, offer_id)
        await msg.answer(str(offer.id), reply_markup=markup)
    except PromotionalOfferDoesNotExist:
        await msg.answer("Акция не найдена.")
