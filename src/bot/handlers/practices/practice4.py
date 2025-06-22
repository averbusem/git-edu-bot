from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.user_keyboards import menu_keyboard
from src.bot.states.practice_states import Practice4State
from src.bot.utils import settings
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.bot.utils.practice_steps import pre_practice_state
from src.db.database import db

PRACTICE_DATA = get_practice_data(4)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})

router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка создания ветки new_branch."""
    lines = answer.splitlines()
    if "* new_branch" in lines and ("main" in lines or "master" in lines):
        return None
    elif "fatal: not a valid branch name" in answer.lower():
        return "not_valid_branch"
    elif "* new_branch" not in lines:
        return "branch_not_listed"
    return "other"


def check_task2(answer: str) -> str | None:
    """Проверка fast-forward слияния."""
    lines = answer.splitlines()
    if len(lines) >= 2 and (lines[0].startswith(
            "* main") or lines[0].startswith("* master")) and lines[1].startswith("  new_branch"):
        if "Add file.txt" in lines[0] and "Add file.txt" in lines[1]:
            return None
    if "already up-to-date" in answer.lower():
        return "already_up_to_date"
    elif "Add file.txt" not in answer:
        return "no_commit_in_new_branch"
    elif ("* main" in answer or "* master" in answer) and "Add file.txt" not in lines[0]:
        return "no_commit_in_main"
    return "other"


def check_task3(answer: str) -> str | None:
    """Проверка слияния веток new_branch1 и new_branch2."""
    if "Merge made by the" in answer and "file2.txt | 0" in answer and "create mode 100644 file2.txt" in answer:
        return None
    elif "already up-to-date" in answer.lower():
        return "already_up_to_date"
    elif "nothing to commit" in answer.lower():
        return "nothing_to_commit"
    elif "conflict" in answer.lower():
        return "conflict"
    return "other"


def check_task4(answer: str) -> str | None:
    """Проверка перебазирования ветки feature на основную ветку."""
    lines = answer.splitlines()
    if len(lines) >= 2 and "Add feature.txt" in lines[0] and "Update main" in lines[1]:
        return None
    elif "fatal: invalid upstream 'main'" in answer.lower() or "fatal: invalid upstream 'master'" in answer.lower():
        return "invalid_upstream"
    elif "Add feature.txt" not in answer:
        return "files_missing"
    elif "Merge" in answer:
        return "non_linear_history"
    return "other"


def check_task5(answer: str) -> str | None:
    """Проверка переноса коммита (cherry-pick)."""
    lines = answer.splitlines()
    if len(lines) >= 2 and (lines[0].endswith("(HEAD -> main) Add file2.txt") or lines[0].endswith(
            "(HEAD -> master) Add file2.txt")) and (lines[1].endswith("Update main") or lines[1].endswith("Update master")):
        return None
    elif "fatal: bad revision" in answer.lower():
        return "bad_revision"
    elif "Add file2.txt" not in answer:
        return "file_missing"
    return "other"


@router.callback_query(F.data == "practice4")
async def practice4_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    await pre_practice_state(callback_query=callback_query, state=state, user_id=user_id, cur_activity_num=4,
                             practice_state=Practice4State(), practice_name=PRACTICE_NAME)


@router.callback_query(F.data == "start_practice", Practice4State.START)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice4State.TASK1)
    task_data = TASKS["task1"]
    text = "".join(task_data["task_text"])
    await callback_query.message.edit_text(text)


@router.message(Practice4State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task1"]

    error_key = check_task1(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice4State.TASK2)
    task2_data = TASKS["task2"]
    text2 = "".join(task2_data["task_text"])
    await message.answer(text2)


@router.message(Practice4State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task2"]

    error_key = check_task2(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice4State.TASK3)
    task3_data = TASKS["task3"]
    text3 = "".join(task3_data["task_text"])
    await message.answer(text3)


@router.message(Practice4State.TASK3)
async def handle_practice_answer3(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task3"]

    error_key = check_task3(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice4State.TASK4)
    task4_data = TASKS["task4"]
    text4 = "".join(task4_data["task_text"])
    await message.answer(text4)


@router.message(Practice4State.TASK4)
async def handle_practice_answer4(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task4"]

    error_key = check_task4(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice4State.TASK5)
    task5_data = TASKS["task5"]
    text5 = "".join(task5_data["task_text"])
    await message.answer(text5)


@router.message(Practice4State.TASK5)
async def handle_practice_answer5(message: Message, state: FSMContext):
    user_answer = message.text
    task_data = TASKS["task5"]

    error_key = check_task5(user_answer)
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()

    user_id = str(message.from_user.id)
    has_done = (await db.get_current_practice(user_id) > 4)
    await db.update_current_activity(user_id=str(user_id), current_practice=5)

    if not has_done:
        await db.update_points(user_id=user_id, points=settings.PRACTICE_POINTS)
        return await message.answer(
            f"✅ Поздравляем! Вы успешно выполнили все задания практики\n\nВы получили {settings.PRACTICE_POINTS} 🔆",
            reply_markup=menu_keyboard())
    else:
        return await message.answer(f"✅ Поздравляем! Вы успешно повторили все задания практики\n\n",
                                    reply_markup=menu_keyboard())
