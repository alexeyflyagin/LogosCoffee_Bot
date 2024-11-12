
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, PromotionalOfferDoesNotExist
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.presentation.bots.admin_bot.handlers.utils import unknown_error, reset_state, \
    get_file_data
from src.presentation.bots.admin_bot.keyboards import PromotionalOfferCD, promotional_offer_markup
from src.presentation.bots.admin_bot.states import MainStates, MakePromotionalOffer
from src.presentation.checks import checks
from src.presentation.checks.exceptions import ContentTypeException
from src.presentation.resources import strings

router = Router()
admin_service: AdminService


@router.message(MainStates.Main, F.text == strings.BTN.WRITE_PROMOTIONAL_OFFER)
async def create_promotional_offer_handler(msg: Message, state: FSMContext):
    await state.set_state(MakePromotionalOffer.Content)
    await msg.answer(strings.ADMIN.MAKE_OFFER.ENTER_CONTENT, reply_markup=ReplyKeyboardRemove())

@router.message(MakePromotionalOffer.Content)
async def create_promotional_offer__content__handler(msg: Message, state: FSMContext):
    try:
        checks.check_content_type(msg, ContentType.TEXT, ContentType.PHOTO)
        text = msg.text
        preview_photo = None
        if msg.content_type == ContentType.PHOTO:
            text = msg.caption
            preview_photo = get_file_data(msg.bot.token, msg.photo[-1].file_id)
        res = await admin_service.create_promotional_offer(text, preview_photo)
        await show_promotional_offer(msg, res.id)
        await reset_state(msg, state, strings.GENERAL.SELECT_ACTION)
    except ContentTypeException as e:
        await msg.answer(e.msg)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)


@router.callback_query(PromotionalOfferCD.filter())
async def promotional_offer_callback(callback: CallbackQuery, state: FSMContext):
    data = PromotionalOfferCD.unpack(callback.data)
    try:
        if data.action == data.Action.PUBLISH:
            await admin_service.start_promotional_offer(data.offer_id)
            await callback.message.edit_text(callback.message.text + "\n\n(опубликованно)", reply_markup=None)
            await callback.answer("успешно опубликовано") # TODO поменять надписи
        elif data.action == data.Action.DELETE:
            await admin_service.delete_promotional_offer(data.offer_id)
            await callback.answer("успешно удаленно")
    except PromotionalOfferDoesNotExist:
        await callback.answer("Акция не найдена.")
    except (DatabaseError, UnknownError):
        await unknown_error(callback.message, state)


async def show_promotional_offer(msg: Message, offer_id: int):
    try:
        offer = await admin_service.get_promotional_offer(offer_id)
        markup = promotional_offer_markup(offer_id)
        await msg.answer(str(offer.id), reply_markup=markup)
    except PromotionalOfferDoesNotExist:
        await msg.answer("Акция не найдена.")
