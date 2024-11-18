import math
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.resources import strings

PREFIX__LIST = "lst"
MAX_PAGE_SIZE = 6

class ListCD(CallbackData, prefix=PREFIX__LIST):
    tag: str
    page_index: int
    p_arg: Any
    s_arg: Any
    action: int
    selected_item_id: int | None = None

    class Action:
        NEXT_PAGE = 0
        PREVIOUS_PAGE = 1
        COUNTER = 2
        ADD = 3
        SELECT = 4
        BACK = 5


class ListItem:
    def __init__(self, name: str, item_id: int, obj: Any | None = None):
        self.name = name
        self.item_id = item_id
        self.obj = obj


def list_keyboard(tag: str, pg_index: int, pg_count: int, pg_items: list[ListItem],
                  add_btn_text: str | None = strings.BTN.ADD, back_btn_text: str | None = None,
                  p_arg: Any = None, s_arg: Any = None) -> InlineKeyboardMarkup:
    kbb = InlineKeyboardBuilder()
    adjust = []
    if pg_count > 1:
        page_previous_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                                    action=ListCD.Action.PREVIOUS_PAGE).pack()
        page_counter_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                                   action=ListCD.Action.COUNTER).pack()
        page_next_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                                action=ListCD.Action.NEXT_PAGE).pack()
        kbb.add(
            InlineKeyboardButton(text=strings.BTN.PAGE_PREVIOUS, callback_data=page_previous_data),
            InlineKeyboardButton(text=strings.BTN.PAGE_COUNTER.format(current=str(pg_index + 1), all=pg_count),
                                 callback_data=page_counter_data),
            InlineKeyboardButton(text=strings.BTN.PAGE_NEXT, callback_data=page_next_data))
        adjust.append(3)
    for i in pg_items:
        item_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                           action=ListCD.Action.SELECT, selected_item_id=i.item_id).pack()
        kbb.add(InlineKeyboardButton(text=i.name, callback_data=item_data))
    if pg_items:
        adjust.append(len(pg_items))
    if add_btn_text:
        add_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                          action=ListCD.Action.ADD).pack()
        kbb.add(InlineKeyboardButton(text=add_btn_text, callback_data=add_data))
        adjust.append(1)
    if back_btn_text:
        back_data = ListCD(tag=tag, page_index=pg_index, p_arg=p_arg, s_arg=s_arg,
                           action=ListCD.Action.BACK).pack()
        kbb.add(InlineKeyboardButton(text=add_btn_text, callback_data=back_data))
        adjust.append(1)
    return kbb.as_markup()


def get_pages(items: list[ListItem]) -> list[list[ListItem]]:
    page_count = math.ceil(len(items) / MAX_PAGE_SIZE)
    if page_count == 0:
        return [[]]
    return [items[i * MAX_PAGE_SIZE:i * MAX_PAGE_SIZE + MAX_PAGE_SIZE] for i in range(page_count)]


def get_safe_page_index(page_index: int, page_count: int) -> int:
    if page_index >= page_count:
        page_index = page_index % page_count
    elif page_index < 0:
        page_index = page_count - abs(page_index) % page_count
    return page_index
