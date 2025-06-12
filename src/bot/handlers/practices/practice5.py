from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.user_keyboards import menu_keyboard
from src.bot.states.practice_states import Practice5State
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.bot.utils.practice_steps import pre_practice_state
from src.db.database import db

PRACTICE_DATA = get_practice_data(5)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})

router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка вывода git remote -v"""
    if "fatal: not a git repository" in answer:
        return "invalid_directory"
    elif answer == "-":
        return "empty_output"
    elif "origin https://github.com/" in answer and "(fetch)" in answer and "origin https://github.com/" in answer and "(push)" in answer:
        return None
    return "other"


def check_task2(answer: str) -> str | None:
    """Проверка вывода 'git log'"""
    if "fatal: not a git repository" in answer:
        return "invalid_directory"
    elif "fatal: ambiguous argument 'origin/main': unknown revision or path not in the working tree" in answer:
        return "invalid_names"
    elif "commit" in answer and "(HEAD -> main, origin/main, origin/HEAD)" in answer and "Author:" in answer and "Date:" in answer:
        if "Add file.txt" in answer:
            return None
        else:
            return "invalid_message"
    return "other"


def check_task3(answer: str) -> str | None:
    """Проверка вывода 'git status'"""
    if "fatal: not a git repository" in answer:
        return "invalid_directory"
    elif "Your branch is behind" in answer:
        return "branch_is_behind"
    elif "fatal: unable to access" in answer:
        return "connection_problem"
    elif "On branch master" in answer and "Your branch is up to date with 'origin/master'" in answer and "nothing to commit, working tree clean" in answer:
        return None
    return "other"


def check_task4(answer: str) -> str | None:
    """Проверка вывода 'git branch -r'"""
    if "fatal: not a git repository" in answer:
        return "invalid_directory"
    elif "origin/HEAD -> origin/main" in answer and "origin/main" in answer:
        if "origin/newbranch" in answer:
            return None
        else:
            return "branch_missing"
    return "other"


def check_task5(answer: str) -> str | None:
    """Проверка вывода 'git diff main origin/main'"""
    if "fatal: not a git repository" in answer:
        return "invalid_directory"
    elif answer == "-":
        return "empty_output"
    elif "+" in answer:
        if "The last task" in answer:
            return None
        else:
            return "invalid_text"
    return "other"


@router.callback_query(F.data == "practice5")
async def practice5_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    await pre_practice_state(callback_query=callback_query, state=state, user_id=user_id, cur_activity_num=5,
                             practice_state=Practice5State(), practice_name=PRACTICE_NAME)


@router.callback_query(F.data == "start_practice", Practice5State.START)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice5State.TASK1)
    task_data = TASKS["task1"]
    text = "".join(task_data["task_text"])
    await callback_query.message.edit_text(text)


@router.message(Practice5State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task1"]

    error_key = check_task1(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice5State.TASK2)
    task2_data = TASKS["task2"]
    text2 = "".join(task2_data["task_text"])
    await message.answer(text2)


@router.message(Practice5State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task2"]

    error_key = check_task2(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice5State.TASK3)
    task3_data = TASKS["task3"]
    text3 = "".join(task3_data["task_text"])
    await message.answer(text3)


@router.message(Practice5State.TASK3)
async def handle_practice_answer3(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task3"]

    error_key = check_task3(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice5State.TASK4)
    task4_data = TASKS["task4"]
    text4 = "".join(task4_data["task_text"])
    await message.answer(text4)


@router.message(Practice5State.TASK4)
async def handle_practice_answer4(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task4"]

    error_key = check_task4(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice5State.TASK5)
    task5_data = TASKS["task5"]
    text5 = "".join(task5_data["task_text"])
    await message.answer(text5)


@router.message(Practice5State.TASK5)
async def handle_practice_answer5(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task5"]

    error_key = check_task5(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()
    await db.update_current_activity(user_id=str(message.from_user.id), current_practice=6)
    return await message.answer("✅ Поздравляем! Вы успешно выполнили все задания практики", reply_markup=menu_keyboard())
