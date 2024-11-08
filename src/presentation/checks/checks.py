from aiogram.types import Message

from src.presentation.checks.exceptions import ContentTypeException


def check_content_type(msg: Message, *args):
    if msg.content_type not in args:
        raise ContentTypeException(msg.content_type, args)
