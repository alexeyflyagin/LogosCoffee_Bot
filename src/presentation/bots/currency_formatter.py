from decimal import Decimal
from enum import Enum

from babel.numbers import format_currency

DEFAULT_LOCALE = "ru_RU"

class Currency(Enum):
    RUB = "RUB"

def to_currency(amount: Decimal, currency: Currency):
    """
    Convert the amount to currency format.

    :param amount: Number of money (Decimal)
    :param currency: The currency format (Currency)
    :return: The formatted string: 1234567.89 -> 1 234 567,89 ₽
    """
    return format_currency(number=amount, currency=currency.value, locale=DEFAULT_LOCALE)

def to_rub(amount: Decimal) -> str:
    return to_currency(amount=amount, currency=Currency.RUB)