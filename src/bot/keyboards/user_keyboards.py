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


def theory_list_keyboard():
    keyboard = InlineKeyboardBuilder()
    lessons = [
        ("1. Введение в Git", "theory1"),
        ("2. Установка и настройка Git", "theory2"),
        ("3. Основы работы с Git", "theory3"),
        ("4. Ветвление и слияние", "theory4"),
        ("5. Работа с удалёнными репозиториями", "theory5"),
        ("6. Отмена изменений и исправление ошибок", "theory6"),
        ("7. Продвинутые возможности Git", "theory7"),
        ("8. Работа в команде (если успеем)", "theory8"),
        ("9. Интеграция с другими инструментами (если успеем)", "theory9"),
    ]

    for title, callback_data in lessons:
        keyboard.add(InlineKeyboardButton(text=title, callback_data=callback_data))

    keyboard.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

    keyboard.adjust(1)
    return keyboard.as_markup()


def next_massage_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Далее", callback_data=f"next"))
    return keyboard.as_markup()


def tests_list_keyboard():
    keyboard = InlineKeyboardBuilder()
    lessons = [
        ("Тест 1", "test1"),
        ("Тест 2", "test2"),
        ("Тест 3", "test3"),
        ("Тест 4", "test4"),
        ("Тест 5", "test5"),
        ("Тест 6", "test6"),
        ("Тест 7", "test7"),
        ("Тест 8", "test8"),
        ("Тест 9", "test9"),
    ]

    for title, callback_data in lessons:
        keyboard.add(InlineKeyboardButton(text=title, callback_data=callback_data))

    keyboard.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

    keyboard.adjust(1)
    return keyboard.as_markup()


def answer_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="A", callback_data="A"),
        InlineKeyboardButton(text="B", callback_data="B"),
        InlineKeyboardButton(text="C", callback_data="C"),
        InlineKeyboardButton(text="D", callback_data="D"),
    )
    return keyboard.as_markup()


def start_test_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Пройти тест", callback_data="start_test")
    keyboard.button(text="Главное меню", callback_data="main_menu")
    return keyboard.as_markup()


def practice_list_keyboard():
    keyboard = InlineKeyboardBuilder()
    practices = [
        ("Практика 2. Установка и настройка Git", "practice2"),
        ("Практика 3. Создание репозитория и первые коммиты", "practice3"),
        ("Практика 4. Ветвление и слияние", "practice4"),
        ("Практика 5", "practice5"),
        ("Практика 6", "practice6"),
        ("Практика 7", "practice7"),
        ("Практика 8", "practice8"),
        ("Практика 9", "practice9"),
    ]

    for title, callback_data in practices:
        keyboard.add(InlineKeyboardButton(text=title, callback_data=callback_data))

    keyboard.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))

    keyboard.adjust(1)
    return keyboard.as_markup()


def start_practice_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Пройти практику", callback_data="start_practice")
    keyboard.button(text="Главное меню", callback_data="main_menu")
    return keyboard.as_markup()
