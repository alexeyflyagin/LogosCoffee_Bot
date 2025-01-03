from src.data.logoscoffee.exceptions import EmptyTextError, InvalidPhoneNumberError


def check_text_is_not_empty(text: str):
    if text.strip() == "":
        raise EmptyTextError()


def check_phone_number(phone_number: str):
    if phone_number.strip() == "":
        raise InvalidPhoneNumberError(phone_number=phone_number)
