from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    Main = State()


class MakeAnnouncement(StatesGroup):
    Content = State()


class ChangeMenu(StatesGroup):
    TextContent = State()
