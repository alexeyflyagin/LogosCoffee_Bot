import asyncio
from typing import Callable, Awaitable, Any

import asyncpg
from asyncpg import Connection
from src.loggers import service_logger as logger

from src.data.logoscoffee.events.exceptions import DuplicateEventHandlerError, SkipHandler
from src.data.logoscoffee.session_manager import SessionManager


class EventListener:
    def __init__(self, channel: str, callback: Callable[[Any], Awaitable[None]]):
        self.channel: str = channel
        self.callback: Callable[[Any], Awaitable[None]] = callback


class EventNotifier:

    def __init__(self, session_manager: SessionManager):
        self._session_manager: SessionManager = session_manager
        self._handlers: dict[str, Callable[[SessionManager, str], Awaitable[Any]]] = dict()
        self._listeners: list[EventListener] = []

    async def run(self):
        connection: Connection = await asyncpg.connect(dsn=self._session_manager.base_url)
        for channel in self._handlers.keys():
            await connection.add_listener(channel, self.__handle_notification)
        logger.debug(f"The event notifier is established: {len(self._handlers)} handler(s).")
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            await connection.close()

    async def __handle_notification(self, connection: Connection, pid, channel: str, payload: str):
        try:
            handler = self._handlers[channel]
            handler_res = await handler(self._session_manager, payload)
        except SkipHandler:
            logger.debug(f"The handler missed an event for '{channel}' channel.")
            return

        listeners = [i for i in self._listeners if i.channel == channel]
        if not listeners:
            logger.debug(f"The listeners missed an event for '{channel}' channel.")

        for listener in listeners:
            await listener.callback(handler_res)

    def add_handler(self, channel: str, callback: Callable[[SessionManager, str], Awaitable[Any]]):
        if channel in self._handlers:
            raise DuplicateEventHandlerError(f"A handler for '{channel}' channel already exists.")
        self._handlers[channel] = callback

    def handler(self, channel: str):
        def decorator(func):
            self.add_handler(channel, func)
            return func

        return decorator

    def add_listener(self, channel: str, callback: Callable[[Any], Awaitable[None]]):
        self._listeners.append(EventListener(channel, callback))

    def listener(self, channel: str):
        def decorator(func):
            self.add_listener(channel, func)
            return func

        return decorator
