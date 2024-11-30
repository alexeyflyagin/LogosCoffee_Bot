# BFM - Bracket Formatting Markup

import re
from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots import constants

REGEX_PATTERN__BREAKERS = r"\{([^{}]+(?:,[^{}]+)*)\}"
REGEX_PATTERN__CONTENT = r"(\w+):\s*([^\s,]+(?:\s+[^\s,]+)*)\s*,?\s*([^,]*)"
REGEX_PATTERN__URL = r"^(https?://)?[\w.-]+\.[a-zA-Z]{2,}([/?#][^\s]*)?$"
MAX_BUTTONS = 6


def is_url_valid(url: str) -> bool:
    return True if re.match(REGEX_PATTERN__URL, url) else False


class BFMItemType(Enum):
    LINK = "link"
    MENU = "menu"


class BFMItem:
    def __init__(self, item_type: str, label: str, value: str | None, raw: str, raw_content: str, start: int,
                 end: int):
        self.item_type = item_type
        self.label = label
        self.value = value
        self.raw = raw
        self.raw_content = raw_content
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"BMFItem(type={self.item_type}, label={self.label}, value={self.value}, raw={self.raw}, raw_content={self.raw_content}, start={self.start}, end={self.end})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def get_list_from_text(text: str) -> list['BFMItem']:
        """
        :param text: text with bfm items
        :return: The list of instances of BFM items
        """
        matches = re.finditer(REGEX_PATTERN__BREAKERS, text)
        items = []
        for match in matches:
            match2 = re.search(REGEX_PATTERN__CONTENT, match.group(1))
            if not match2:
                continue
            item_type, label, value = list(match2.groups(0))
            if item_type not in [item.value for item in BFMItemType]:
                continue
            if item_type == BFMItemType.LINK.value and not is_url_valid(value):
                continue
            if value.strip() == '':
                value = None
            new_item = BFMItem(
                item_type=item_type,
                label=label,
                value=value,
                raw=match.group(0),
                raw_content=match.group(1),
                start=match.start(),
                end=match.end(),
            )
            items.append(new_item)
        return items


def get_markup(text: str) -> InlineKeyboardMarkup | None:
    """
    :param text: text with bfm items
    :return: The instance of InlineKeyboardMarkup or None if bfm items are not found
    """
    items = BFMItem.get_list_from_text(text)
    if not items:
        return None
    ikb = InlineKeyboardBuilder()
    ikb.max_width = 1
    for i in range(min(MAX_BUTTONS, len(items))):
        item = items[i]
        if item.item_type == BFMItemType.MENU.value:
            ikb.add(InlineKeyboardButton(text=item.label, callback_data=constants.CALLBACK_DATA__LIST_MENU))
        elif item.item_type == BFMItemType.LINK.value:
            ikb.add(InlineKeyboardButton(text=item.label, url=item.value))
    return ikb.as_markup()


def clean_text(text: str) -> str:
    """
    :param text: text with bfm items
    :return: The cleaned text: Welcome! {menu: Go to menu} -> Welcome!
    """
    items = BFMItem.get_list_from_text(text)
    cleaned_text = text
    for i in items:
        cleaned_text = cleaned_text.replace(i.raw, '', 1)
    return cleaned_text.strip()
