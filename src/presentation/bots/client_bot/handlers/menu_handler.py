from html import escape

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, ProductIsNotAvailable, \
    RemovingProductIsNotFound
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.presentation.bots.admin_bot.handlers.utils import unknown_error_for_callback
from src.presentation.bots.client_bot import constants
from src.presentation.bots.client_bot.constants import TAG__LIST_MENU
from src.presentation.bots.client_bot.handlers.utils import unknown_error, get_account_id
from src.presentation.bots.client_bot.states import MainStates
from src.presentation.bots.constants import CALLBACK_DATA__LIST_MENU
from src.presentation.bots.currency_formatter import to_rub
from src.presentation.bots.list_markup import list_keyboard, get_pages, ListItem, ListCD
from src.presentation.bots.utils import send_or_update_msg
from src.presentation.resources import strings

router = Router()
client_service: ClientService
order_service: ClientOrderService


class ProductCD(CallbackData, prefix=constants.PREFIX__PRODUCT):
    product_id: int
    action: int

    class Action:
        ADD = 0
        REMOVE = 1
        ADDED = 2
        UNAVAILABLE = 3


def get_product_markup(product_id: int, is_available: bool = True, added_counter: int = 0) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    adjust = []
    if is_available:
        if added_counter:
            remove_data = ProductCD(product_id=product_id, action=ProductCD.Action.REMOVE).pack()
            added_data = ProductCD(product_id=product_id, action=ProductCD.Action.ADDED).pack()
            add_data = ProductCD(product_id=product_id, action=ProductCD.Action.ADD).pack()
            ikb.add(InlineKeyboardButton(text=strings.BTN.REMOVE_SYMBOL, callback_data=remove_data))
            ikb.add(InlineKeyboardButton(text=strings.BTN.ADDED_TO_DRAFT_ORDER.format(counter=added_counter), callback_data=added_data))
            ikb.add(InlineKeyboardButton(text=strings.BTN.ADD_SYMBOL, callback_data=add_data))
            adjust.append(3)
        else:
            add_data = ProductCD(product_id=product_id, action=ProductCD.Action.ADD).pack()
            ikb.add(InlineKeyboardButton(text=strings.BTN.ADD_TO_DRAFT_ORDER, callback_data=add_data))
            adjust.append(1)
    else:
        unavailable_data = ProductCD(product_id=product_id, action=ProductCD.Action.UNAVAILABLE).pack()
        ikb.add(InlineKeyboardButton(text=strings.BTN.PRODUCT_TEMPORARY_UNAVAILABLE, callback_data=unavailable_data))
        adjust.append(1)
    ikb.adjust(*adjust)
    return ikb.as_markup()

@router.message(MainStates.Main, F.text == strings.BTN.MENU)
async def menu_handler(msg: Message, state: FSMContext):
    try:
        await show_menu(msg)
    except (DatabaseError, UnknownError):
        await unknown_error(msg, state)

@router.callback_query(F.data == CALLBACK_DATA__LIST_MENU)
async def open_menu_callback(callback: CallbackQuery, state: FSMContext):
    try:
        await show_menu(callback.message)
        await callback.answer()
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)

@router.callback_query(ListCD.filter())
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    data = ListCD.unpack(callback.data)
    try:
        client_id = await get_account_id(state)
        if data.action == data.Action.SELECT:
            await show_product(callback.message, data.selected_item_id, client_id=client_id)
            await callback.answer()
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)

@router.callback_query(ProductCD.filter())
async def product_callback(callback: CallbackQuery, state: FSMContext):
    data = ProductCD.unpack(callback.data)
    try:
        client_id = await get_account_id(state)
        if data.action == data.Action.ADD:
            await order_service.add_to_draft_order(client_id, data.product_id)
            await show_product(callback.message, data.product_id, is_update=True, client_id=client_id)
            await callback.answer()
        elif data.action == data.Action.REMOVE:
            await order_service.remove_from_draft_order(client_id, data.product_id)
            await show_product(callback.message, data.product_id, is_update=True, client_id=client_id)
            await callback.answer()
        elif data.action == data.Action.ADDED:
            await callback.answer()
        elif data.action == data.Action.UNAVAILABLE:
            await callback.answer(text=strings.CLIENT.PRODUCT.ADD.IS_NOT_AVAILABLE)
    except RemovingProductIsNotFound:
        await callback.answer(text=strings.CLIENT.PRODUCT.REMOVE.IS_NOT_FOUND)
    except ProductIsNotAvailable:
        await callback.answer(text=strings.CLIENT.PRODUCT.ADD.IS_NOT_AVAILABLE)
    except (DatabaseError, UnknownError):
        await unknown_error_for_callback(callback, state)


async def show_menu(msg: Message, page_index: int = 0, is_update: bool = False):
    products = await client_service.get_menu()
    all_products_s = []
    items = []
    for i in range(len(products.all_products)):
        items.append(ListItem(str(i + 1), item_id=products.all_products[i].id, obj=products.all_products[i]))
    pages = get_pages(items)
    markup = list_keyboard(tag=TAG__LIST_MENU, pg_index=page_index, pg_count=len(pages), pg_items=pages[page_index],
                           add_btn_text=None)
    for i in range(len(pages[page_index])):
        all_products_s.append(strings.CLIENT.MENU.ITEM.format(
            index=i + 1,
            product_name=products.all_products[i].product_name,
            price=to_rub(products.all_products[i].price),
        ))
    text = strings.CLIENT.MENU.PAGE.format(items='\n'.join(all_products_s))
    await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=markup)

async def show_product(msg: Message, product_id: int, is_update: bool = False, client_id: int | None = None):
    product = await client_service.get_product_by_id(product_id)
    added_counter = 0
    if client_id:
        added_counter = await order_service.get_count_of_product_from_draft_order(client_id, product_id)
    markup = get_product_markup(product_id, product.is_available, added_counter)
    text = strings.CLIENT.PRODUCT.MAIN.format(
        product_name=escape(product.product_name),
        price=to_rub(product.price),
        description=escape(product.description),
    )
    await send_or_update_msg(msg, text=text, is_update=is_update, replay_markup=markup)