from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (answer_keyboard, menu_keyboard,
                                              start_test_keyboard)
from src.bot.states.test_states import Test2State
from src.bot.utils.data_loader import get_test_data
from src.bot.utils.test_formatter import (format_question_summary,
                                          format_question_text)
from src.db.database import db

OPTIONS = ["A", "B", "C", "D"]
TEST_DATA = get_test_data(2)
TEST_NAME = TEST_DATA.get("test_name", "")
QUESTIONS = TEST_DATA.get("questions", {})


router = Router()


@router.callback_query(F.data == "test2")
async def test2_selected(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    current_test = int(await db.get_current_activity(user_id=user_id, activity="test"))
    if current_test < 2:
        await callback_query.message.edit_text("Вы ещё не прошли предыдущие тесты\n\n"
                                               "Возвращайтесь, когда выполните всё до этого теста",
                                               reply_markup=menu_keyboard())
    else:
        await state.set_state(Test2State.QUESTION1)
        await callback_query.message.edit_text(
            f"Вы выбрали тест по теме: <b>{TEST_NAME}</b>\n\n"
            "📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.",
            reply_markup=start_test_keyboard(),
        )


@router.callback_query(F.data == "start_test", Test2State.QUESTION1)
async def send_test_question1(callback_query: CallbackQuery, state: FSMContext):
    question_data = QUESTIONS["question1"]
    text = format_question_text(question_data)
    await callback_query.message.edit_text(text, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION1)
async def handle_test_answer1(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question1"]
    summary_text = format_question_summary(question_data, user_answer)

    # Здесь можно добавить код для записи результата в базу данных.
    # Например, если результат правильный, записать True, иначе False.
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=1, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION2)
    question2_data = QUESTIONS["question2"]
    text2 = format_question_text(question2_data)
    await callback_query.message.answer(text2, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION2)
async def handle_test_answer2(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question2"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 2
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=2, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION3)
    question3_data = QUESTIONS["question3"]
    text3 = format_question_text(question3_data)
    await callback_query.message.answer(text3, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION3)
async def handle_test_answer3(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question3"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 3
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=3, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION4)
    question4_data = QUESTIONS["question4"]
    text4 = format_question_text(question4_data)
    await callback_query.message.answer(text4, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION4)
async def handle_test_answer4(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question4"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 4
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=4, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION5)
    question5_data = QUESTIONS["question5"]
    text5 = format_question_text(question5_data)
    await callback_query.message.answer(text5, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION5)
async def handle_test_answer5(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question5"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 5
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=5, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION6)
    question6_data = QUESTIONS["question6"]
    text6 = format_question_text(question6_data)
    await callback_query.message.answer(text6, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION6)
async def handle_test_answer6(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question6"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 6
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=6, is_correct=result)

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test2State.QUESTION7)
    question7_data = QUESTIONS["question7"]
    text7 = format_question_text(question7_data)
    await callback_query.message.answer(text7, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test2State.QUESTION7)
async def handle_test_answer7(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    question_data = QUESTIONS["question7"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 7
    result = 1 if user_answer == question_data["correct"] else 0
    await db.tick_question_answer(user_id=user_id, test_number=2, question_number=7, is_correct=result)
    await db.set_test_mark(user_id=user_id, test_number=2)
    await db.update_current_activity(user_id=user_id, current_test=3)

    test_mark = await db.get_test_mark(user_id=user_id, test_number=2)

    await callback_query.message.edit_text(summary_text)
    await callback_query.message.answer(f"Тест завершён. Ваша оценка за тест {test_mark}\n\n Спасибо за участие!",
                                        reply_markup=menu_keyboard())
