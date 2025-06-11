from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import (answer_keyboard, menu_keyboard,
                                              start_test_keyboard)
from src.bot.states.test_states import Test1State
from src.bot.utils.data_loader import get_test_data
from src.bot.utils.test_formatter import format_question_text
from src.bot.utils.test_steps import process_test_answer
from src.db.database import db

OPTIONS = ["A", "B", "C", "D"]
TEST_DATA = get_test_data(1)
TEST_NAME = TEST_DATA.get("test_name", "")
QUESTIONS = TEST_DATA.get("questions", {})

router = Router()


@router.callback_query(F.data == "test1")
async def test1_selected(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Test1State.QUESTION1)
    user_id = callback_query.from_user.id
    await db.start_test(user_id=str(user_id), test_number=1)
    test_mark = await db.get_test_mark(user_id=str(user_id), test_number=1)
    if test_mark is None:
        await callback_query.message.edit_text(
            f"Вы выбрали тест по теме: <b>{TEST_NAME}</b>\n\n"
            "📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.\n"
            "❗ Помните, что оценка ставится по мере прохождения теста и исправить её уже нельзя!",
            reply_markup=start_test_keyboard(),
        )
    else:
        await callback_query.message.edit_text(
            f"Вы выбрали тест по теме: <b>{TEST_NAME}</b>\n\n"
            f"📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.\n\n"
            f"❗ Вы уже проходили этот тест до конца\n"
            f"Ваша оценка <b>{test_mark}%</b>",
            reply_markup=start_test_keyboard(),
        )


@router.callback_query(F.data == "start_test", Test1State.QUESTION1)
async def send_test_question1(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    previous_results = await db.get_test_results(user_id=str(user_id), test_number=1)
    marks_cur_test = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
    await state.update_data(cur_marks=marks_cur_test)
    await state.update_data(prev_results=previous_results)
    question_data = QUESTIONS["question1"]
    text = format_question_text(question_data)
    await callback_query.message.edit_text(text, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION1)
async def handle_test_answer1(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question1",
        question_number=1,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION2,
        next_question_key="question2"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION2)
async def handle_test_answer2(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question2",
        question_number=2,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION3,
        next_question_key="question3"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION3)
async def handle_test_answer3(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question3",
        question_number=3,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION4,
        next_question_key="question4"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION4)
async def handle_test_answer4(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question4",
        question_number=4,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION5,
        next_question_key="question5"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION5)
async def handle_test_answer5(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question5",
        question_number=5,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION6,
        next_question_key="question6"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION6)
async def handle_test_answer6(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(
        callback_query,
        state,
        test_number=1,
        question_key="question6",
        question_number=6,
        questions=QUESTIONS,
        next_state=Test1State.QUESTION7,
        next_question_key="question7"
    )


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION7)
async def handle_test_answer7(callback_query: CallbackQuery, state: FSMContext):
    await process_test_answer(callback_query, state, test_number=1, question_key="question7", question_number=7,
                              questions=QUESTIONS)
    user_id = callback_query.from_user.id
    has_done = (await db.get_current_test(user_id) > 1)
    await db.set_test_mark(user_id=str(user_id), test_number=1)
    await db.update_current_activity(user_id=str(user_id), current_test=2)

    state_data = await state.get_data()
    cur_results = state_data["cur_marks"]
    answers = cur_results
    total = len(answers)
    correct_count = sum(1 for v in answers.values() if v)
    score = round((correct_count / total) * 100, 2) if total else 0.0

    if not has_done:
        points = round(score / 100 * settings.TEST_POINTS)
        await db.update_points(user_id=str(user_id), points=points)
        await callback_query.message.answer(f"Тест завершён на оценку <b>{score}%</b>\n\nВы получили {points} 🔆 Спасибо за участие!",
                                            reply_markup=menu_keyboard())
    else:
        await callback_query.message.answer(
            f"Тест завершён на оценку <b>{score}%</b>\n\nСпасибо за повторное прохождение!",
            reply_markup=menu_keyboard())
