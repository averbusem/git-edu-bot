from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import answer_keyboard
from src.bot.utils.test_formatter import (format_question_summary,
                                          format_question_text)
from src.db.database import db


async def process_test_answer(callback_query: CallbackQuery, state: FSMContext, test_number: int,
                              question_key: str, question_number: int, questions: dict,
                              next_state=None, next_question_key: str = None):
    user_answer = callback_query.data
    user_id = callback_query.from_user.id
    results = await state.get_data()
    question_data = questions[question_key]
    summary_text = format_question_summary(question_data, user_answer)

    key = str(question_number)
    if key not in results:
        is_correct = 1 if user_answer == question_data["correct"] else 0
        await db.tick_question_answer(user_id=user_id, test_number=test_number, question_number=question_number,
                                      is_correct=is_correct)
        results[key] = is_correct
        await state.update_data(results)

    await callback_query.message.edit_text(summary_text)
    if next_state and next_question_key:
        await state.set_state(next_state)
        next_data = questions[next_question_key]
        next_text = format_question_text(next_data)
        await callback_query.message.answer(next_text, reply_markup=answer_keyboard())
