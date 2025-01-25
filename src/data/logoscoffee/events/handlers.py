import logging

from src.data.logoscoffee.dao import dao_client_account
from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, OrderEntity, \
    ClientAccountEntity
from src.data.logoscoffee.events.channels import NEW_REVIEW_CHANNEL, NEW_DISTRIBUTED_ANNOUNCEMENT, NEW_ORDER
from src.data.logoscoffee.events.exceptions import SkipHandler
from src.data.logoscoffee.session_manager import SessionManager
from src.di.container import di

notifier = di.event_notifier()


@notifier.handler(channel=NEW_REVIEW_CHANNEL)
async def new_review_handler(session_manager: SessionManager, payload: str):
    return ReviewEntity.model_validate_json(payload)


@notifier.handler(channel=NEW_DISTRIBUTED_ANNOUNCEMENT)
async def new_review_handler(session_manager: SessionManager, payload: str):
    announcement = AnnouncementEntity.model_validate_json(payload)
    if not announcement.date_last_distribute:
        raise SkipHandler()
    return announcement


@notifier.handler(channel=NEW_ORDER)
async def new_order_handler(session_manager: SessionManager, payload: str):
    try:
        order = OrderEntity.model_validate_json(payload)
        async with session_manager.get_session() as s:
            client = await dao_client_account.get_by_id(s, order.client_id)
            client_entity = ClientAccountEntity.model_validate(client)
            order.client = client_entity
        return order
    except Exception as e:
        logging.error(e)
        raise SkipHandler()
