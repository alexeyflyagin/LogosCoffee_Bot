from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    Main = State()

class MakePromotionalOffer(StatesGroup):
    Content = State()
