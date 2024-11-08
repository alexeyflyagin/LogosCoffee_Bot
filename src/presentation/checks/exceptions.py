from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import random_str


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
            msg=random_str(strings.ERRORS.CONTENT_TYPE)
        )