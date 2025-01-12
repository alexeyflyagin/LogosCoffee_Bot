from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity
from src.data.logoscoffee.events.channels import NEW_REVIEW_CHANNEL, NEW_DISTRIBUTED_ANNOUNCEMENT
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
