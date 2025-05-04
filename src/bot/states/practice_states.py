from aiogram.fsm.state import State, StatesGroup


class Practice2State(StatesGroup):
    TASK1 = State()
    TASK2 = State()


class Practice3State(StatesGroup):
    TASK1 = State()
    TASK2 = State()
    TASK3 = State()
    TASK4 = State()