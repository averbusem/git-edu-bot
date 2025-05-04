import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              start_practice_keyboard)
from src.bot.states.practice_states import Practice3State
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.db.database import db

PRACTICE_DATA = get_practice_data(3)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})


router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка создания репозитория."""
    if "fatal: not a git repository" in answer.lower():
        return "not_rep"
    elif "reinitialized" in answer.lower():
        return "reinit"
    elif "Initialized empty Git repository in" in answer:
        return None
    return "other"


def check_task2(answer: str) -> str | None:
    """Проверка вывода при добавлении hello.txt в индекс."""
    if "Changes to be committed:" in answer and "new file:   hello.txt" in answer:
        if "deleted:    hello.txt" not in answer:
            return None
        else:
            return "delete_error"
    elif "fatal: not a git repository" in answer.lower():
        return "not_rep"
    elif "pathspec" in answer.lower():
        return "pathspec"
    elif "nothing to commit" in answer.lower():
        return "no_add"
    elif "Changes to be committed:" in answer and "new file:   hello.txt" not in answer:
        return "wrong_file"
    return "other"


def check_task3(answer: str) -> str | None:
    """Проверка создания коммита."""
    head_line = next((line for line in answer.splitlines() if "HEAD -> " in line), None)
    if head_line and head_line.endswith("Add hello.txt"):
        return None
    elif head_line and not(head_line.endswith("Add hello.txt")):
        return "commit_name_error"
    elif "fatal: not a git repository" in answer.lower():
        return "not_rep"
    elif "nothing to commit, working tree clean" in answer.lower():
        return "commit_error"
    elif "Initial commit" in answer and "nothing to commit" in answer:
        return "no_commit"
    elif "Author identity unknown" in answer:
        return "aut_error"
    elif "# Please enter the commit message for your changes" in answer:
        return "new_terminal"
    return "other"


def check_task4(answer: str) -> str | None:
    """Проверка вывода истории коммитов."""

    if len(answer.splitlines()) != 2:
        return "one_commit"
    head_line = answer.splitlines()[0]
    sec_line =  answer.splitlines()[1]
    if head_line.endswith("Update hello.txt") and sec_line.endswith("Add hello.txt"):
        return None
    elif not(head_line.endswith("Update hello.txt") and sec_line.endswith("Add hello.txt")):
        return "commit_name_error"
    elif "fatal: not a git repository" in answer.lower():
        return "not_rep"
    elif "nothing to commit, working tree clean" in answer.lower():
        return "commit_error"
    elif "Initial commit" in answer and "nothing to commit" in answer:
        return "no_commit"
    elif "Author identity unknown" in answer:
        return "aut_error"
    elif "# Please enter the commit message for your changes" in answer:
        return "new_terminal"
    return "other"


@router.callback_query(F.data == "practice3")
async def practice1_selected(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice3State.TASK1)
    await callback_query.message.edit_text(
        f"Вы выбрали практику по теме: <b>{PRACTICE_NAME}</b>\n\n"
        "📝 Вы можете сделать задания, чтобы проверить свои знания или вернуться в главное меню.",
        reply_markup=start_practice_keyboard(),
    )


@router.callback_query(F.data == "start_practice", Practice3State.TASK1)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    task_data = TASKS["task1"]
    text = task_data["task_text"]
    await callback_query.message.edit_text(text)


@router.message(Practice3State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task1"]

    error_key = check_task1(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice3State.TASK2)

    task2_data = TASKS["task2"]
    text2 = task2_data["task_text"]
    await message.answer(text2)

@router.message(Practice3State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task2"]

    error_key = check_task2(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice3State.TASK3)

    task3_data = TASKS["task3"]
    text3 = task3_data["task_text"]
    await message.answer(text3)

@router.message(Practice3State.TASK3)
async def handle_practice_answer3(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task3"]

    error_key = check_task3(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice3State.TASK4)

    task4_data = TASKS["task4"]
    text4 = task4_data["task_text"]
    await message.answer(text4)

@router.message(Practice3State.TASK4)
async def handle_practice_answer4(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task4"]

    error_key = check_task4(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()
    await db.update_current_activity(user_id=message.from_user.id, current_practice=4)
    await message.answer("✅ Поздравляем! Вы успешно выполнили все задания практики",
                         reply_markup=menu_keyboard())