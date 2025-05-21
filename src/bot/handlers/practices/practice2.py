import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.handlers import settings
from src.bot.handlers.keyboards.user_keyboards import (menu_keyboard,
                                                       start_practice_keyboard)
from src.bot.states.practice_states import Practice2State
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.db.database import db

PRACTICE_DATA = get_practice_data(2)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})


router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка вывода `git --version`."""
    expected = TASKS["task1"]["expected"]  # "git 2.49.0 или выше"
    if "command not found" in answer.lower():
        return "command_not_found"
    version_mask = re.search(r"(\d+)\.(\d+)\.(\d+)", answer)
    if version_mask:
        version = tuple(map(int, version_mask.groups()))
        requirement = tuple(map(int, expected.split()[1].split(".")))
        if version < requirement:
            return "version_lower"
        else:
            return None
    return "other"


def check_task2(answer: str) -> str | None:
    """Проверка вывода `git config --list --name-only`."""
    got = set(line.strip() for line in answer.splitlines() if line.strip())
    expected = set(TASKS["task2"]["expected"])  # ["user.email","user.name"]
    missing = expected - got
    if "user.email" in missing:
        return "no_user.email"
    if "user.name" in missing:
        return "no_user.name"
    return None


@router.callback_query(F.data == "practice2")
async def practice1_selected(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice2State.TASK1)
    await callback_query.message.edit_text(
        f"Вы выбрали практику по теме: <b>{PRACTICE_NAME}</b>\n\n"
        "📝 Вы можете сделать задания, чтобы проверить свои знания или вернуться в главное меню.",
        reply_markup=start_practice_keyboard(),
    )


@router.callback_query(F.data == "start_practice", Practice2State.TASK1)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    task_data = TASKS["task1"]
    text = task_data["task_text"]
    await callback_query.message.edit_text(text)


@router.message(Practice2State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task1"]

    error_key = check_task1(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice2State.TASK2)

    task2_data = TASKS["task2"]
    text2 = task2_data["task_text"]
    await message.answer(text2)


@router.message(Practice2State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task2"]

    error_key = check_task2(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()
    await db.update_points(user_id=message.from_user.id, points=settings.PRACTICE_POINTS)
    await message.answer(f"✅ Поздравляем! Вы успешно выполнили все задания практики\n\n Вы получили {settings.PRACTICE_POINTS} опыта.",
                         reply_markup=menu_keyboard())
