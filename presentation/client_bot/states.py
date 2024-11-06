from aiogram.fsm.state import StatesGroup, State

class LoginStates(StatesGroup):
    PressButton = State()
    EnterName = State()

class MainStates(StatesGroup):
    Main = State()

class EnterReviewStates(StatesGroup):
    EnterText = State()
