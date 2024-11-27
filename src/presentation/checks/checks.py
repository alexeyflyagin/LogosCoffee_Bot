from aiogram.types import Message

from src.presentation.checks.exceptions import ContentTypeError, MessageContentCountError


def check_content_type(msg: Message, *args):
    if msg.content_type not in args:
        raise ContentTypeError(msg.content_type, args)

def check_one_msg(msg_count: int):
    if msg_count != 1:
        raise MessageContentCountError(1, msg_count)
