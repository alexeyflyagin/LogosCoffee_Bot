from textwrap import dedent

from presentation.strings_builder import b, code, i, random_str, StrGroup

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
    AUTHORIZE = "Авторизоваться 🔑"
    WRITE_REVIEW = "Написать отзыв ⭐"



class GENERAL(StrGroup):
    ACTION_CANCELED = "Действие отменено 👌"

    CANCEL_ACTION = "Отменить дейстиве - /cancel"

    SELECT_ACTION = "Выберите действие."

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

    class AUTHORIZATION(StrGroup):
        PRESS_BTN = f"""Для авторизации потребуется твой номер телефона. Нажмите '{b(BTN.AUTHORIZE)}', чтобы продолжить."""

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
        ENTER_REVIEW_CONTENT = dedent(f"""\
            Введите текст отзыва ✍️ {i('(Отзыв будет отправлен анонимно)')}
            {GENERAL.CANCEL_ACTION}
        """)

        class REVIEW__COOLDOWN_ERROR(StrGroup):
            V1 = dedent("""\
                Благодарим за ваши отзывы! 🙏 
                Недавно вы уже делились мнением. Пожалуйста, попробуйте чуть позже ⏳
            """)

            V2 = dedent("""\
                Ваше мнение для нас важно! 🙌 
                Но недавно вы уже отправили отзыв. Попробуйте ещё раз немного позже ⏳
            """)

            V3 = dedent("""\
                Спасибо за ваш отзыв! 😊 
                Мы его уже получили недавно. Попробуйте отправить ещё один немного позже ⏳
            """)

            V4 = dedent("""\
                Мы ценим ваш отзыв! 🙏 
                Но пока что не можем принять новый. Пожалуйста, попробуйте чуть позже ⏳
            """)

            V5 = dedent("""\
                Спасибо за обратную связь! 🙏
                Мы недавно уже получили от вас отзыв. Попробуйте снова немного позже ⏳
            """)

        class SUCCESSFUL(StrGroup):
            V1 = f"{b('Большое спасибо за ваш отзыв!')} Это помогает нам становиться лучше! 😊"

            V2 = f"{b('Ваш отзыв очень ценен для нас!')} Спасибо, что помогаете нам расти! 😊"

            V3 = f"{b('Спасибо за ваш отклик!')} Мы работаем над улучшениями, и ваш отзыв важен! ✨"
