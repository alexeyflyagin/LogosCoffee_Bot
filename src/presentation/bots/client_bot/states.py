from aiogram.fsm.state import StatesGroup, State

class AuthorizationStates(StatesGroup):
    PressButton = State()
    EnterName = State()

class MainStates(StatesGroup):
    Main = State()

class EnterReviewStates(StatesGroup):
    EnterText = State()
