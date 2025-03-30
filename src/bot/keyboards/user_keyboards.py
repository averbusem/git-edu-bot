from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard():
    # Начальная клавиатура с основными кнопками
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Учиться", callback_data="learn_button"),
                 InlineKeyboardButton(text="Практиковаться", callback_data="practice_button"))
    keyboard.row(InlineKeyboardButton(text="Прогресс", callback_data="progress_button"))
    return keyboard.as_markup()


def menu_keyboard():
    # Клавиатура для возврата в меню (аналогично команде /start)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return keyboard.as_markup()


def practice_choice_keyboard():
    # Клавиатура для выбора типа практики или возврата в главное меню
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Тесты", callback_data="choice_tests"),
                 InlineKeyboardButton(text="Задания", callback_data="choice_tasks"))
    keyboard.row(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return keyboard.as_markup()
