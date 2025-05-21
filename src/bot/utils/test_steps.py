from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers.keyboards.user_keyboards import (answer_keyboard,
                                                       menu_keyboard,
                                                       start_test_keyboard)
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


async def pre_test_state(callback_query: CallbackQuery, state: FSMContext, user_id: int, test_number: int,
                         cur_activity_num: int, test_state, test_name: str,):
    current_activity = await db.get_current_activity(user_id=user_id)
    cur_test = current_activity["test"]
    cur_theory = current_activity["theory"]
    cur_practice = current_activity["practice"]
    if any([cur_theory < cur_activity_num, cur_test <
           cur_activity_num, cur_practice < cur_activity_num]):
        await callback_query.message.edit_text("❗️Вы ещё не прошли предыдущий урок\n\n"
                                               "Возвращайтесь, когда выполните всё в предыдущих уроках",
                                               reply_markup=menu_keyboard())
    else:
        await state.set_state(test_state.QUESTION1)
        await db.start_test(user_id=user_id, test_number=test_number)
        test_mark = await db.get_test_mark(user_id=user_id, test_number=test_number)
        if test_mark is None:
            await callback_query.message.edit_text(
                f"Вы выбрали тест по теме: <b>{test_name}</b>\n\n"
                "📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.\n"
                "❗ Помните, что оценка ставится по мере прохождения теста и исправить её уже нельзя!",
                reply_markup=start_test_keyboard(),
            )
        else:
            await callback_query.message.edit_text(
                f"Вы выбрали тест по теме: <b>{test_name}</b>\n\n"
                f"📝 Вы можете пройти тест, чтобы проверить свои знания или вернуться в главное меню.\n\n"
                f"❗ Вы уже проходили этот тест до конца\n"
                f"Ваша оценка <b>{test_mark}</b>",
                reply_markup=start_test_keyboard(),
            )
