from datetime import timedelta


class LCError(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return self._message


class InvalidTokenError(LCError):
    def __init__(self, token: str | None):
        super().__init__(f"The token ({token}) is incorrect.")


class InvalidPhoneNumberError(LCError):
    def __init__(self, phone_number: str | None):
        super().__init__(f"The phone number ({phone_number}) is incorrect.")


class DatabaseError(LCError):
    def __init__(self, e: Exception):
        super().__init__(f"The database error occurred: {e}")


class UnknownError(LCError):
    def __init__(self, e: Exception):
        super().__init__(f"Occurred an unexpected error: {e}")


class TokenGenerateError(LCError):
    def __init__(self):
        super().__init__("Token generation was wrong")


class EmptyTextError(LCError):
    def __init__(self):
        super().__init__(f"Review content is empty")


class CooldownError(LCError):
    def __init__(self, left_time: timedelta):
        super().__init__(f"Action attempted before cooldown period has elapsed.")
        self.left_time = left_time


class AlreadySubscribedError(LCError):
    def __init__(self, user_state_id: int, event_name: str):
        super().__init__(f"Already is subscribed to this event('{event_name}'): {user_state_id}")


class AlreadyUnsubscribedError(LCError):
    def __init__(self, user_state_id: int, event_name: str):
        super().__init__(f"Already is unsubscribed to this event('{event_name}'): {user_state_id}")


class AnnouncementNotFoundError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"Announcement ({kwargs}) does not exist")


class PlacedOrderIsEmptyError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"Order ({kwargs}), which was tried to place, is empty")


class ProductIsNotAvailableError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"Product ({kwargs}) is not available")


class OrderStateError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"Order state ({kwargs}) was unexpected")


class ProductNotFoundError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"The product ({kwargs}) you tried to find doesn't exist")


class OrderNotFoundError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"The order ({kwargs}) doesn't exist")


class OtherOrderIsPlacedAlreadyError(LCError):
    def __init__(self, **kwargs):
        super().__init__(f"Other order ({kwargs}) is already placed. New order can't be placed now")
