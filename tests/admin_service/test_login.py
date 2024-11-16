from datetime import datetime
from unittest.mock import MagicMock, AsyncMock

import loguru
import pytest
import pytest_asyncio

from src import config
from src.data.logoscoffee.services.admin_service_impl import AdminServiceImpl


@pytest_asyncio.fixture
def session_manager_mock():
    return MagicMock()


@pytest_asyncio.fixture
def admin_service(session_manager_mock):
    return AdminServiceImpl(session_manager=session_manager_mock)


@pytest.mark.asyncio
async def test_login_success(admin_service, session_manager_mock, mocker):
    mock_session = AsyncMock()
    session_manager_mock.get_session.return_value.__aenter__.return_value = mock_session

    mock_result = MagicMock()
    mock_session.execute.return_value = mock_result

    mock_scalars = MagicMock()
    mock_account = MagicMock()
    mock_account.date_authorized = None
    mock_result.scalars.return_value = mock_scalars
    mock_scalars.first.return_value = mock_account

    mock_entity = MagicMock()
    mocker.patch('src.data.logoscoffee.entities.orm_entities.AdminAccountEntity.model_validate', return_value=mock_entity)

    result = await admin_service.login(config.DEFAULT_ADMIN_KEY_FOR_LOGIN)

    mock_session.execute.assert_called_once()
    mock_account.date_authorized = datetime.now()
    mock_session.flush.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result == mock_entity

