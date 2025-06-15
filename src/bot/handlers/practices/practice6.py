from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.user_keyboards import menu_keyboard
from src.bot.states.practice_states import Practice6State
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.bot.utils.practice_steps import pre_practice_state
from src.db.database import db

PRACTICE_DATA = get_practice_data(6)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})

router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка вывода 'git status' после git restore test.txt"""
    if "nothing to commit, working tree clean" in answer:
        return None
    elif "Changes not staged for commit" in answer:
        return "changes_not_staged"
    elif "deleted:" in answer:
        return "file_deleted"
    return "other"


def check_task2(answer: str) -> str | None:
    """Проверка вывода 'git log -1 --pretty=oneline' после amend"""
    if "Add newTest" in answer and "(HEAD -> " in answer:
        return None
    elif "Add newTest" in answer and "HEAD" not in answer:
        return "new_commit_created"
    return "other"


def check_task3(answer: str) -> str | None:
    """Проверка вывода 'git log --oneline -n 1' после revert"""
    if "Revert \"Add task3.txt\"" in answer:
        return None
    elif "conflict" in answer.lower():
        return "conflict"
    return "other"


def check_task4(answer: str) -> str | None:
    """Проверка содержимого task4.txt после reset hard и восстановления"""
    if "Critical Data" in answer:
        return None
    elif "fatal" or "bad revision" in answer.lower():
        return "bad_revision"
    elif "fatal: not a git repository" in answer:
        return "commit_not_found"
    elif answer.strip() != "Critical Data":
        return "wrong_recovery"
    return "other"


def check_task5(answer: str) -> str | None:
    """Проверка содержимого conflict.txt после merge с обоими вариантами"""
    lines = [line.strip() for line in answer.splitlines() if line.strip()]
    if "Ariana" in lines and "Taylor" in lines and "Kendrick":
        return None
    elif "Merge conflict" in answer:
        return "merge_failed"
    return "other"


def check_task6(answer: str) -> str | None:
    """Проверка вывода 'git status' после merge --abort"""
    if "nothing to commit, working tree clean" in answer:
        return None
    elif "Unmerged paths" in answer:
        return "unmerged_paths"
    elif "You are not currently on a branch" in answer:
        return "wrong_branch"
    elif "There is no merge to abort" in answer:
        return "no_merge"
    return "other"


@router.callback_query(F.data == "practice6")
async def practice6_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    await pre_practice_state(
        callback_query=callback_query,
        state=state,
        user_id=user_id,
        cur_activity_num=6,
        practice_state=Practice6State(),
        practice_name=PRACTICE_NAME,
    )


@router.callback_query(F.data == "start_practice", Practice6State.START)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice6State.TASK1)
    text = "".join(TASKS["task1"]["task_text"])
    await callback_query.message.edit_text(text)


@router.message(Practice6State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    error_key = check_task1(message.text)
    task_data = TASKS["task1"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice6State.TASK2)
    text = "".join(TASKS["task2"]["task_text"])
    await message.answer(text)


@router.message(Practice6State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    error_key = check_task2(message.text)
    task_data = TASKS["task2"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice6State.TASK3)
    text = "".join(TASKS["task3"]["task_text"])
    await message.answer(text)


@router.message(Practice6State.TASK3)
async def handle_practice_answer3(message: Message, state: FSMContext):
    error_key = check_task3(message.text)
    task_data = TASKS["task3"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice6State.TASK4)
    text = "".join(TASKS["task4"]["task_text"])
    await message.answer(text)


@router.message(Practice6State.TASK4)
async def handle_practice_answer4(message: Message, state: FSMContext):
    error_key = check_task4(message.text)
    task_data = TASKS["task4"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice6State.TASK5)
    text = "".join(TASKS["task5"]["task_text"])
    await message.answer(text)


@router.message(Practice6State.TASK5)
async def handle_practice_answer5(message: Message, state: FSMContext):
    error_key = check_task5(message.text)
    task_data = TASKS["task5"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice6State.TASK6)
    text = "".join(TASKS["task6"]["task_text"])
    await message.answer(text)


@router.message(Practice6State.TASK6)
async def handle_practice_answer6(message: Message, state: FSMContext):
    error_key = check_task6(message.text)
    task_data = TASKS["task6"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()
    await db.update_current_activity(
        user_id=str(message.from_user.id),
        current_practice=7
    )
    await message.answer(
        "✅ Поздравляем! Вы успешно выполнили все задания практики",
        reply_markup=menu_keyboard()
    )
