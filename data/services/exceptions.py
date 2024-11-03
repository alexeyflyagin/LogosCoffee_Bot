class LCException(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return self._message


class InvalidToken(LCException):
    def __init__(self, token: str):
        super().__init__(f"The token was not found: {token}")


class DatabaseError(LCException):
    def __init__(self, e: Exception):
        super().__init__(f"The database error occurred: {e}")


class UnknownError(LCException):
    def __init__(self, e: Exception):
        super().__init__(f"Occurred an unexpected error: {e}")

