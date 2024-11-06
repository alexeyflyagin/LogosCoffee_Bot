from aiogram.types import BotCommand

from presentation.client_bot.commands import CANCEL_COMMAND


def command(c: BotCommand) -> str:
    return f"/{c.command}"


CHECK__CONTENT_TYPE_ERROR = "Некорректный тип данных."


LOG_IN__TOKEN_WAS_NOT_ENTERED = "Войти не удалось: токен не найден. Введите токен."

LOG_IN__INVALID_TOKEN = "Войти не удалось: неверный токен."

UNKNOWN_ERROR = "Что-то пошло не так"

LOG_IN__SUCCESSFUL = "Вход успешно выполнен"

CANCEL_ACTION = "Действие отменено."

ADVICE_CANCEL = f"Чтобы отменить - {command(CANCEL_COMMAND)}"


BTN_AUTHORIZE = "Авторизоваться"


CLIENT_AUTHORIZE_STATE1_MSG = f"Для авторизации нажмите: '{BTN_AUTHORIZE}'"

CLIENT_AUTHORIZE_STATE1__USER_MISMATCH = "Это не твой контакт."

CLIENT_URLS = "Ссылки: https://www.com"

CLIENT__LOG_IN__SUCCESSFUL = "МОЛОДЕЦ"

CLIENT__REVIEW__ENTER_TEXT = f"""Введите текст отзыва
{ADVICE_CANCEL}"""

CLIENT__REVIEW__ANSWER = "Спасибо за отзыв"

CLIENT__REVIEW__COOLDOWN_ERROR = "Нельзя отправлять отзывы так часто! Подождите хотя бы денёк..."

CLIENT__REVIEW__EMPTY_TEXT_ERROR = "Текст отзыва отсутствует"

CLIENT__SELECT_ACTION = "Выберите действие."