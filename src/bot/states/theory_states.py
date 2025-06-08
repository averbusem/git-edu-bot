from aiogram.fsm.state import State, StatesGroup


class Theory1State(StatesGroup):
    # MESSAGE1 = State()
    MESSAGE2 = State()
    MESSAGE3 = State()


class Theory2State(StatesGroup):
    MESSAGE2 = State()
    MESSAGE3 = State()


class Theory3State(StatesGroup):
    MESSAGE2 = State()
    MESSAGE3 = State()
    MESSAGE4 = State()


class Theory4State(StatesGroup):
    MESSAGE2 = State()
    MESSAGE3 = State()
    MESSAGE4 = State()
    MESSAGE5 = State()
