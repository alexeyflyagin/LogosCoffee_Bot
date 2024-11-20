from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup

from src.presentation.bots.constants import CALLBACK_DATA__LIST_MENU
from src.presentation.resources import strings

BS_FEATURES = 'html.parser'

TAG__URL_BTN = 'url-btn'
TAG__MENU_BTN = 'menu-btn'

ARG__URL = 'url'
MAX_ROW_IN_MARKUP = 12


class MagicHTMLParser:

    def __init__(self, text: str):
        self._text = text

    @property
    def markup(self) -> InlineKeyboardMarkup:
        soup = BeautifulSoup(self._text, BS_FEATURES)
        tag_elements = soup.find_all((TAG__URL_BTN, TAG__MENU_BTN))
        ikb = InlineKeyboardBuilder()
        adjust = []
        for tag_index in range(min(MAX_ROW_IN_MARKUP, len(tag_elements))):
            tag = tag_elements[tag_index]
            url = tag.get(ARG__URL)
            callback_data = None
            btn_text = tag.text or strings.BTN.BUTTON
            if tag.name == TAG__MENU_BTN:
                callback_data = CALLBACK_DATA__LIST_MENU
                btn_text = tag.text or strings.BTN.MENU
            if url or callback_data:
                ikb.add(InlineKeyboardButton(text=btn_text, url=url, callback_data=callback_data))
                adjust.append(1)
        ikb.adjust(*adjust)
        return ikb.as_markup()

    @property
    def clean_text(self) -> str:
        soup = BeautifulSoup(self._text, BS_FEATURES)
        btn_elements = soup.find_all((TAG__URL_BTN, TAG__MENU_BTN))
        for tag in btn_elements:
            tag.decompose()
        return soup.text

    @property
    def text(self):
        return self.text
