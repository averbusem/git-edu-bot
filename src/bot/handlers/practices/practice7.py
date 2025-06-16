from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.user_keyboards import menu_keyboard
from src.bot.states.practice_states import Practice7State
from src.bot.utils.data_loader import get_practice_data
from src.bot.utils.practice_formatter import format_task_feedback
from src.bot.utils.practice_steps import pre_practice_state
from src.db.database import db

PRACTICE_DATA = get_practice_data(7)
PRACTICE_NAME = PRACTICE_DATA.get("practice_name", "")
TASKS = PRACTICE_DATA.get("tasks", {})

router = Router()


def check_task1(answer: str) -> str | None:
    """Проверка вывода 'git status' после git restore test.txt"""
    if "stash@{0}: On main: First stash" in answer:
        return None
    elif not answer.strip():
        return "empty_output"
    elif "stash" not in answer:
        return "no_stash"
    return "other"


def check_task2(answer: str) -> str | None:
    if "HSE" in answer.upper(): 
        return None 
    elif answer.strip() == "-": 
        return "empty_output" 
    return "other"


def check_task3(answer: str) -> str | None:
    if "One.txt:TaskOne GIT" in answer and "Three.txt:TaskThree GIT" in answer: 
       return None 
    elif not answer.strip(): 
       return "empty_output" 
    return "other"


def check_task4(answer: str) -> str | None:
    if answer.strip().startswith("1)") and "BLUE" in answer:
        return None
    elif "No such file or directory" in answer or "not found" in answer:
        return "file_not_found"
    elif "fatal:" in answer.lower():
        return "wrong_line"
    return "other"



@router.callback_query(F.data == "practice7")
async def practice7_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    await pre_practice_state(
        callback_query=callback_query,
        state=state,
        user_id=user_id,
        cur_activity_num=7,
        practice_state=Practice7State(),
        practice_name=PRACTICE_NAME,
    )


@router.callback_query(F.data == "start_practice", Practice7State.START)
async def send_practice_question1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Practice7State.TASK1)
    text = "".join(TASKS["task1"]["task_text"])
    await callback_query.message.edit_text(text)

@router.message(Practice7State.TASK1)
async def handle_practice_answer1(message: Message, state: FSMContext):
    error_key = check_task1(message.text)
    task_data = TASKS["task1"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice7State.TASK2)
    text = "".join(TASKS["task2"]["task_text"])
    await message.answer(text)


@router.message(Practice7State.TASK2)
async def handle_practice_answer2(message: Message, state: FSMContext):
    error_key = check_task2(message.text)
    task_data = TASKS["task2"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice7State.TASK3)
    text = "".join(TASKS["task3"]["task_text"])
    await message.answer(text)


@router.message(Practice7State.TASK3)
async def handle_practice_answer3(message: Message, state: FSMContext):
    error_key = check_task3(message.text)
    task_data = TASKS["task3"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.set_state(Practice7State.TASK4)
    text = "".join(TASKS["task4"]["task_text"])
    await message.answer(text)


@router.message(Practice7State.TASK4)
async def handle_practice_answer4(message: Message, state: FSMContext):
    error_key = check_task4(message.text)
    task_data = TASKS["task4"]
    if error_key:
        await message.answer(format_task_feedback(task_data, error_key))
        return

    await state.clear()
    await db.update_current_activity(
        user_id=str(message.from_user.id),
        current_practice=8
    )
    await message.answer(
        "✅ Поздравляем! Вы успешно выполнили все задания практики",
        reply_markup=menu_keyboard()
    )