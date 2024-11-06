from aiogram.fsm.state import StatesGroup, State

class LoginStates(StatesGroup):
    EnterName = State()

class MainStates(StatesGroup):
    Main = State()