from datetime import datetime, timedelta


class LCException(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return self._message

class InvalidKey(LCException):
    def __init__(self, key: str):
        super().__init__(f"The key was not found: {key}")

class DatabaseError(LCException):
    def __init__(self, e: Exception):
        super().__init__(f"The database error occurred: {e}")

class UnknownError(LCException):
    def __init__(self, e: Exception):
        super().__init__(f"Occurred an unexpected error: {e}")

class TokenGenerateError(LCException):
    def __init__(self):
        super().__init__("Token generation was wrong")

class EmptyTextError(LCException):
    def __init__(self):
        super().__init__(f"Review content is empty")

class CooldownError(LCException):
    def __init__(self, left_time: timedelta):
        super().__init__(f"Action attempted before cooldown period has elapsed.")
        self.left_time = left_time

class AlreadySubscribedError(LCException):
    def __init__(self, user_state_id: int, event_name: str):
        super().__init__(f"Already is subscribed to this event('{event_name}'): {user_state_id}")

class AlreadyUnsubscribedError(LCException):
    def __init__(self, user_state_id: int, event_name: str):
        super().__init__(f"Already is unsubscribed to this event('{event_name}'): {user_state_id}")

class AnnouncementNotFound(LCException):
    def __init__(self, **kwargs):
        super().__init__(f"Announcement ({kwargs}) does not exist")

class PlacedOrderIsEmpty(LCException):
    def __init__(self, **kwargs):
        super().__init__(f"Order ({kwargs}), which was tried to place, is empty")

class ProductIsNotAvailable(LCException):
    def __init__(self, **kwargs):
        super().__init__(f"Product ({kwargs}) is not available")

class OrderStateError(LCException):
    def __init__(self, **kwargs):
        super().__init__(f"Order state ({kwargs}) was unexpected")

class RemovingProductIsNotFound(LCException):
    def __init__(self, **kwargs):
        super().__init__(f"Product ({kwargs}) you tried to remove doesn't exist in the draft order")