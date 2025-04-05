from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (answer_keyboard, menu_keyboard,
                                              start_test_keyboard)
from src.bot.states.test_states import Test1State
from src.bot.utils.data_loader import get_test_data
from src.bot.utils.test_formatter import (format_question_summary,
                                          format_question_text)

OPTIONS = ["A", "B", "C", "D"]
TEST_DATA = get_test_data(1)
TEST_NAME = TEST_DATA.get("test_name", "")
QUESTIONS = TEST_DATA.get("questions", {})


router = Router()


@router.callback_query(F.data == "test1")
async def test1_selected(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Test1State.QUESTION1)
    await callback_query.message.edit_text(
        f"Вы выбрали тест по теме: <b>{TEST_NAME}</b>\n\n"
        "📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.",
        reply_markup=start_test_keyboard(),
    )


@router.callback_query(F.data == "start_test", Test1State.QUESTION1)
async def send_test_question1(callback_query: CallbackQuery, state: FSMContext):
    question_data = QUESTIONS["question1"]
    text = format_question_text(question_data)
    await callback_query.message.edit_text(text, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION1)
async def handle_test_answer1(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question1"]
    summary_text = format_question_summary(question_data, user_answer)

    # Здесь можно добавить код для записи результата в базу данных.
    # Например, если результат правильный, записать True, иначе False.
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION2)
    question2_data = QUESTIONS["question2"]
    text2 = format_question_text(question2_data)
    await callback_query.message.answer(text2, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION2)
async def handle_test_answer2(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question2"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 2
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION3)
    question3_data = QUESTIONS["question3"]
    text3 = format_question_text(question3_data)
    await callback_query.message.answer(text3, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION3)
async def handle_test_answer3(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question3"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 3
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION4)
    question4_data = QUESTIONS["question4"]
    text4 = format_question_text(question4_data)
    await callback_query.message.answer(text4, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION4)
async def handle_test_answer4(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question4"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 4
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION5)
    question5_data = QUESTIONS["question5"]
    text5 = format_question_text(question5_data)
    await callback_query.message.answer(text5, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION5)
async def handle_test_answer5(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question5"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 5
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION6)
    question6_data = QUESTIONS["question6"]
    text6 = format_question_text(question6_data)
    await callback_query.message.answer(text6, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION6)
async def handle_test_answer6(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question6"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 6
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    await state.set_state(Test1State.QUESTION7)
    question7_data = QUESTIONS["question7"]
    text7 = format_question_text(question7_data)
    await callback_query.message.answer(text7, reply_markup=answer_keyboard())


@router.callback_query(F.data.in_(OPTIONS), Test1State.QUESTION7)
async def handle_test_answer7(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data
    question_data = QUESTIONS["question7"]
    summary_text = format_question_summary(question_data, user_answer)

    # Запись результата для вопроса 7
    # result = True if user_answer == question_data["correct"] else False

    await callback_query.message.edit_text(summary_text)
    # Тест завершён – здесь можно добавить итоговое сообщение или сохранить общий результат
    await callback_query.message.answer("Тест завершён. Спасибо за участие!",
                                        reply_markup=menu_keyboard())
