from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str


class CheckError(Exception):
    def __init__(self, log_msg: str, msg: str):
        self.log_msg = log_msg
        self.msg = msg

    def __str__(self) -> str:
        return self.log_msg


class ContentTypeError(CheckError):
    def __init__(self, msg_type: str, available_types: tuple[str, ...]):
        super().__init__(
            log_msg=f"Wrong content type - {msg_type}. excepted: {available_types}",
            msg=random_str(strings.ERRORS.CONTENT_TYPE)
        )

class MessageContentCountError(CheckError):
    def __init__(self, msg_count_expected: int, received_count: int):
        super().__init__(
            log_msg=f"{msg_count_expected} message was expected, but received: {received_count}",
            msg=random_str(strings.ERRORS.CONTENT_TYPE)
        )