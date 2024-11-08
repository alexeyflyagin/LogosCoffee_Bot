from dependency_injector import containers, providers
import src.config
from src import config

from src.data.logoscoffee.db.session_manager_impl import SessionManagerImpl
from src.data.logoscoffee.services.admin_service_impl import AdminServiceImpl
from src.data.logoscoffee.services.client_service_impl import ClientServiceImpl
from src.data.logoscoffee.services.employee_service_impl import EmployeeServiceImpl
from src.data.logoscoffee.services.user_state_service_impl import UserStateServiceImpl


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


container = Container()
container.config.DB_URL.from_value(config.DB_URL)
