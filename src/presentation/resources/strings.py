from textwrap import dedent

from src.presentation.resources.strings_builder.strings_builder import b, i, StrGroup, code, quote

CAFE_NAME = "LOGOSCOFFEE"


class ERRORS(StrGroup):
    class UNKNOWN(StrGroup):
        V1 = "😧 Упс! Что-то пошло не по плану. Пожалуйста, повторите попытку."

        V2 = "🙁 Что-то не сработало. Повторите попытку, пожалуйста."

        V3 = "🙁 Ой, что-то пошло не так. Попробуйте снова чуть позже!"

        V4 = "😟 Упс, произошёл сбой. Пожалуйста, попробуйте снова."

        V5 = "😣 Что-то не сработало, извините за неудобство. Повторите попытку!"

        V6 = "🙁 К сожалению, возникла ошибка. Попробуйте ещё раз позже."

    class CONTENT_TYPE(StrGroup):
        V1 = "🤔 Хм, кажется, это не совсем то, что я ожидал... Попробуйте снова!"

        V2 = "🙃 Хм, похоже, это не то, что я ждал. Попробуйте снова!"

        V3 = "🤨 Это немного не то. Попробуйте отправить другой формат."

        V4 = "🤔 Хм, странно. Я ожидал что-то другое. Попробуйте ещё раз, пожалуйста!"

        V5 = "😅 Ой! Это что-то другое. Пожалуйста, отправьте нужный формат."


class BTN(StrGroup):
    AUTHORIZE = "🔑 Авторизоваться"
    WRITE_REVIEW = "💬 Написать отзыв"
    WRITE_ANNOUNCEMENT = "📢 Новое объявление"
    REVIEWS = "💬 Отзывы"
    MY_ANNOUNCEMENTS = "Архив объявлений"
    DISTRIBUTE = "📢 Разослать"
    SHOW = "👁️ Показать"
    DELETE = "🗑️ Удалить"
    CONFIRM = "✅ Да, всё верно!"
    CANCEL = "❌ Отменить"
    MENU = "📋 Меню"
    MAKE_ORDER = "🍰 Сделать заказать"
    CHANGE_MENU = "✏️ Изменить меню"
    ADD = "+ Добавить"
    ADD_TO_DRAFT_ORDER = "Добавить в корзину"
    PRODUCT_TEMPORARY_UNAVAILABLE = "Продукт временно недоступен!"
    ADD_SYMBOL = "+"
    REMOVE_SYMBOL = "-"
    BUTTON = "Кнопка"
    PAGE_PREVIOUS = "«"
    PAGE_NEXT = "»"
    PAGE_COUNTER = "{current} / {all}"


class GENERAL(StrGroup):
    ACTION_CANCELED = "Действие отменено 👌"

    CANCEL_ACTION = "Отменить дейстиве - /cancel"

    SELECT_ACTION = "Выберите действие."

    NO_DATA = "-"

    class LOGIN(StrGroup):
        TOKEN_WAS_NOT_ENTERED = "Для входа нужен токен! Просто напишите его после /start."

        INVALID_TOKEN = "Упс! Токен неверный. Попробуте снова 🔑"

        class SUCCESSFUL(StrGroup):
            V1 = f"{b('Вы успешно вошли!')} Всё готово к работе 🚀"

            V2 = f"{b('Вы в системе!')} Всё готово для начала работы 🎉"

            V3 = f"{b('Готово!')} Вы успешно вошли, можно начинать 🙌"

            V4 = f"{b('Отлично!')} Вход выполнен, приступим к работе 🌟"


class CLIENT(StrGroup):
    LINKS = "Присоединяйся к нам в vk: https://vk.com/logoscoffee"

    EMPTY_MENU_CONTENT = "Упс! Меню пока что ещё не готово 😣"

    class MAKE_ORDER(StrGroup):
        ENTER_DETAILS = f"✍️ Опишите, что бы вы хотели видеть в заказе...\n_(Перед тем как составить заказ, стоит ознакомиться с меню)_\n{GENERAL.CANCEL_ACTION}"
        ANOTHER_ORDER_ALREADY_PLACED = """Упс! У вас все еще есть незакрытый заказ 🤔"""
        SUCCESS = """☕ Заказ успешно создан и ожидает подтверждения!"""

    class AUTHORIZATION(StrGroup):
        PRESS_BTN = f"""Нажмите '{b(BTN.AUTHORIZE)}', чтобы авторизоваться."""

        CONTACT_NOT_LINKED = "Этот контакт не связан с вашим Telegram аккаунтом. Попробуй ещё раз!"

        class SUCCESSFUL(StrGroup):
            V1 = dedent(f"""\
                {b('Вход выполнен успешно! 🎉')}
                Добро пожаловать в {b(CAFE_NAME)} 😊☕
            """)

            V2 = dedent(f"""\
                {b('Добро пожаловать в ')}{b('CAFE_NAME! 🎉')}
                Пора наслаждаться ароматным кофе! 😊☕
            """)

            V3 = dedent(f"""\
                {b('Вход выполнен успешно! 🎉')}
                Теперь можно наслаждаться любимым кофе вместе с {b(CAFE_NAME)}! ☕✨
            """)

    class REVIEW(StrGroup):
        ENTER_CONTENT = dedent(f"""\
            Введите текст отзыва ✍️ {i('(Отзыв будет отправлен анонимно)')}
            {GENERAL.CANCEL_ACTION}
        """)

        class COOLDOWN_ERROR(StrGroup):
            V1 = "🙏 Благодарим за ваши отзывы! Недавно вы уже делились мнением. Пожалуйста, попробуйте чуть позже ⏳"

            V2 = "🙌 Ваше мнение для нас важно! Но недавно вы уже отправили отзыв. Попробуйте ещё раз немного позже ⏳"

            V3 = "😊 Спасибо за ваш отзыв! Мы его уже получили недавно. Попробуйте отправить ещё один немного позже ⏳"

            V4 = "🙏 Мы ценим ваш отклик! Но пока что не можем принять новый. Пожалуйста, попробуйте чуть позже ⏳"

            V5 = "🙏 Спасибо за обратную связь! Мы недавно уже получили от вас отзыв. Попробуйте снова немного позже ⏳"

        class SUCCESSFUL(StrGroup):
            V1 = f"{b('Большое спасибо за ваш отзыв!')} Это помогает нам становиться лучше! 😊"

            V2 = f"{b('Ваш отзыв очень ценен для нас!')} Спасибо, что помогаете нам расти! 😊"

            V3 = f"{b('Спасибо за ваш отклик!')} Мы работаем над улучшениями, и ваш отзыв важен! ✨"


class ADMIN(StrGroup):
    NEW_REVIEW_NOTIFICATION = dedent(f"""\
        💬 Вы получили новый отзыв!
        —
        {quote('{review_content}')}
    """)

    EMPTY_MENU_CONTENT = "Упс! Меню пока что ещё не готово!"

    class CHANGE_MENU(StrGroup):
        ENTER_CONTENT = f"✍️ *Подготовьте текст для меню.* После того, как удостоверитесь в корректности нового меню, пришлите его мне _(Меню у клиентов сменится сразу)_\n{GENERAL.CANCEL_ACTION}"
        SUCCESS = "👌 Меню успешно изменено!"

    class MAKE_ANNOUNCEMENT(StrGroup):
        ENTER_CONTENT = dedent(f"""\
            ✍️ Отправьте контент объявления. 
            Это должен быть текст. Можете прикрепить одно фото 📸.
            {GENERAL.CANCEL_ACTION}
        """)

        SUCCESSFUL = "Успешно создано"

    class ANNOUNCEMENT(StrGroup):
        MAIN = dedent(f"""\
            {b('Объявление')} {code(f'#{{announcement_id}}')}
            Создано: {{date_create}}
            Последняя рассылка: {{date_last_distribute}}
        """)

        DOES_NOT_EXIST = "Упс... Объявление не найдено."

        BUTTON_MENU_FOR_CLIENT = f"У клиента откроется '{BTN.MENU}' по нажатию на эту кнопку."

        class PUBLISH(StrGroup):
            TOAST_SUCCESSFUL = "Объявление успешно опубликовано!"

            SUCCESSFUL = "👌 Объявление успешно опубликовано!"

            WARNING = dedent(f"""\
                ⚠️ {b(f'Внимание: Проверьте корректность информации в объявлении!')} {i(f'({BTN.CANCEL} » {BTN.SHOW})')}
                После подтверждения, оно будет отправлено всем клиентам.
                
                Вы уверены, что хотите сделать рассылку {b('объявления #{announcement_id}')}?
            """)

            COOLDOWN_ERROR = """Недавно вы уже рассылали объявление. Пожалуйста, попробуйте чуть позже ⏳"""


class EMPLOYEE(StrGroup):
    class ORDER(StrGroup):
        NO_NICKNAME = i("No name")

        IN_PROGRESS_VIEW = dedent(f"""\
            🟢 {b('Заказ #{id}')}  {i('{date}')}
            Получатель: {{nickname}} {i('(id: {client_id})')}
            
            Статус: {{state}}
            —
            {quote('{details}', expandable=True)}
        """)

        CLOSED_VIEW = dedent(f"""\
            {b('Заказ #{id}')}  {i('{date}')}
            Получатель: {{nickname}} {i('(id: {client_id})')}
            
            Статус: {{state}}
            —
            {quote('{details}', expandable=True)}
        """)

        class BTN(StrGroup):
            ORDER_CONFIRM = "✅ Подвердить!"
            ORDER_READY = "➡️ Готов к выдаче!"
            ORDER_COMPLETE = "➡️ Вручён!"
            ORDER_REJECT = "🚫 Отклонить"

        class STATES(StrGroup):
            PENDING = f"{b('⌛️ Ожидает подтверждения')}"
            COOKING = f"{b('👨‍🍳 Готовится...')}"
            READY = f"{b('📦 Готов к выдаче!')}  {b('({code})')}"
            COMPLETED = f"{b('🎉 Завершен')}"
            CANCELED = f"{b('🚫 Отменен')}\n{i('{cancel_details}')}"
