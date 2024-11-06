from data.services.exceptions import EmptyTextError


def check_text_is_not_empty(text: str):
    if text.strip() == "":
        raise EmptyTextError()