from aiogram.types import Message

from src.presentation.checks.exceptions import ContentTypeException, MessageContentCountException


def check_content_type(msg: Message, *args):
    if msg.content_type not in args:
        raise ContentTypeException(msg.content_type, args)

def check_one_msg(msg_count: int):
    if msg_count != 1:
        raise MessageContentCountException(1, msg_count)
