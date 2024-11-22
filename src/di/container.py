from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dependency_injector import containers, providers
from src import config

from src.data.logoscoffee.db.session_manager_impl import SessionManagerImpl
from src.data.logoscoffee.services.admin_service_impl import AdminServiceImpl
from src.data.logoscoffee.services.client_order_service_impl import ClientOrderServiceImpl
from src.data.logoscoffee.services.client_service_impl import ClientServiceImpl
from src.data.logoscoffee.services.employee_service_impl import EmployeeServiceImpl
from src.data.logoscoffee.services.event_service_impl import EventServiceImpl
from src.data.logoscoffee.services.user_state_service_impl import UserStateServiceImpl
from src.presentation.bots.admin_bot.bot import AdminBot
from src.presentation.bots.client_bot.bot import ClientBot
from src.presentation.bots.employee_bot.bot import EmployeeBot
from src.presentation.user_state_storage import UserStateStorage


def client_handlers__inject():
    from src.presentation.bots.client_bot.handlers import handler, authorization_handler, review_handler, end_handler, \
        menu_handler
    authorization_handler.client_service = di.client_service()
    handler.event_service = di.event_service()
    end_handler.client_service = di.client_service()
    review_handler.client_service = di.client_service()
    menu_handler.client_service = di.client_service()
    menu_handler.order_service = di.client_order_service()


def admin_handlers__inject():
    from src.presentation.bots.admin_bot.handlers import handler, end_handler, announcement_handler
    handler.admin_service = di.admin_service()
    handler.event_service = di.event_service()
    announcement_handler.admin_service = di.admin_service()
    end_handler.admin_service = di.admin_service()


def employee_handlers__inject():
    from src.presentation.bots.employee_bot.handlers import handler
    handler.employee_service = di.employee_service()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Database providers
    session_manager = providers.Singleton(
        SessionManagerImpl,
        url=config.DB_URL,
    )

    # Service providers
    client_service = providers.Factory(
        ClientServiceImpl,
        session_manager=session_manager,
    )

    admin_service = providers.Factory(
        AdminServiceImpl,
        session_manager=session_manager,
    )

    employee_service = providers.Factory(
        EmployeeServiceImpl,
        session_manager=session_manager,
    )

    user_state_service = providers.Factory(
        UserStateServiceImpl,
        session_manager=session_manager,
    )

    event_service = providers.Factory(
        EventServiceImpl,
        session_manager=session_manager,
    )

    client_order_service = providers.Factory(
        ClientOrderServiceImpl,
        session_manager=session_manager,
    )

    # Presentation layer
    user_state_storage = providers.Factory(
        UserStateStorage,
        user_state_service=user_state_service,
    )

    dp = providers.Factory(
        Dispatcher,
        storage=user_state_storage,
    )

    bot_for_admin = providers.Factory(
        Bot,
        token=config.ADMIN_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    bot_for_client = providers.Factory(
        Bot,
        token=config.CLIENT_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    bot_for_employee = providers.Factory(
        Bot,
        token=config.EMPLOYEE_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    admin_bot = providers.Factory(
        AdminBot,
        bot=bot_for_admin,
        dp=dp,
    )

    client_bot = providers.Factory(
        ClientBot,
        bot=bot_for_client,
        dp=dp,
    )

    employee_bot = providers.Factory(
        EmployeeBot,
        bot=bot_for_employee,
        dp=dp,
    )


di = Container()

di.config.DB_URL.from_value(config.DB_URL)
di.config.ADMIN_BOT_TOKEN.from_value(config.ADMIN_BOT_TOKEN)
di.config.CLIENT_BOT_TOKEN.from_value(config.CLIENT_BOT_TOKEN)
di.config.EMPLOYEE_BOT_TOKEN.from_value(config.EMPLOYEE_BOT_TOKEN)

client_handlers__inject()
admin_handlers__inject()
employee_handlers__inject()
