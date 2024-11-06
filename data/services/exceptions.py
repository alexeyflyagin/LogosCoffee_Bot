from datetime import datetime, timedelta


class LCException(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return self._message


class InvalidToken(LCException):
    def __init__(self, token: str | None):
        super().__init__(f"The token was not found: {token}")


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
