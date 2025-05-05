from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import answer_keyboard, menu_keyboard
from src.bot.states.test_states import Test3State
from src.bot.utils.data_loader import get_test_data
from src.bot.utils.test_formatter import format_question_text
from src.bot.utils.test_steps import pre_test_state, process_test_answer
from src.db.database import db

OPTIONS = ["A", "B", "C", "D"]
TEST_DATA = get_test_data(3)
TEST_NAME = TEST_DATA.get("test_name", "")
QUESTIONS = TEST_DATA.get("questions", {})


router = Router()


@router.callback_query(F.data == "test3")
async def test3_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await pre_test_state(callback_query, state, user_id,
                         test_number=3, cur_activity_num=3, test_state=Test3State(), test_name=TEST_NAME)


@router.callback_query(F.data == "start_test", Test3State.QUESTION1)
async def send_test_question1(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    previous_results = await db.get_test_results(user_id=user_id, test_number=3)
    marks_cur_test = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
    await state.update_data(cur_marks=marks_cur_test)
    await state.update_data(prev_results=previous_results)
    question_data = QUESTIONS["question1"]
    text = format_question_text(question_data)
    await callback_query.message.edit_text(text, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION1)
async def handle_test_answer1(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question1",
        question_number=1,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION2,
        next_question_key="question2"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION2)
async def handle_test_answer2(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question2",
        question_number=2,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION3,
        next_question_key="question3"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION3)
async def handle_test_answer3(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question3",
        question_number=3,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION4,
        next_question_key="question4"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION4)
async def handle_test_answer4(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question4",
        question_number=4,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION5,
        next_question_key="question5"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION5)
async def handle_test_answer5(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question5",
        question_number=5,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION6,
        next_question_key="question6"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION6)
async def handle_test_answer6(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=3,
        question_key="question6",
        question_number=6,
        questions=QUESTIONS,
        next_state=Test3State.QUESTION7,
        next_question_key="question7"
    )


@router.callback_query(F.data.in_(OPTIONS), Test3State.QUESTION7)
async def handle_test_answer7(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(callback_query, state, test_number=3, question_key="question7", question_number=7,
                              questions=QUESTIONS)
    user_id = callback_query.from_user.id
    await db.set_test_mark(user_id=user_id, test_number=3)
    await db.update_current_activity(user_id=user_id, current_test=4)

    state_data = await state.get_data()
    cur_results = state_data["cur_marks"]
    answers = cur_results
    total = len(answers)
    correct_count = sum(1 for v in answers.values() if v)
    score = round((correct_count / total) * 100, 2) if total else 0.0
    await callback_query.message.answer(f"Тест завершён на оценку <b>{score}%</b>\n\nСпасибо за участие!",
                                        reply_markup=menu_keyboard())
