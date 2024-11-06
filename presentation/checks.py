from aiogram.types import Message

from presentation import strings


class CheckException(Exception):
    def __init__(self, log_msg: str, msg: str):
        self.log_msg = log_msg
        self.msg = msg

    def __str__(self) -> str:
        return self.log_msg


class ContentTypeException(CheckException):
    def __init__(self, msg_type: str, available_types: tuple[str, ...]):
        super().__init__(
            log_msg=f"Wrong content type - {msg_type}. excepted: {available_types}",
            msg=strings.CHECK__CONTENT_TYPE_ERROR
        )


def check_content_type(msg: Message, *args):
    if msg.content_type not in args:
        raise ContentTypeException(msg.content_type, args)
