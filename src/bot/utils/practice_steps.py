from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              start_practice_keyboard)
from src.db.database import db


async def pre_practice_state(callback_query: CallbackQuery, state: FSMContext, user_id: int, cur_activity_num: int,
                             practice_state, practice_name: str):
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
        await state.set_state(practice_state.START)
        if cur_practice < cur_activity_num:
            await callback_query.message.edit_text(
                f"Вы выбрали практику по теме: <b>{practice_name}</b>\n\n"
                "📝 Вы можете пройти практику, чтобы проверить свои знания или вернуться в главное меню.",
                reply_markup=start_practice_keyboard(),
            )
        else:
            await callback_query.message.edit_text(
                f"Вы выбрали практику по теме: <b>{practice_name}</b>\n\n"
                f"📝 Вы можете пройти практику, чтобы проверить свои знания или вернуться в главное меню.\n\n"
                f"❗ Вы уже проходили эту практику до конца",
                reply_markup=start_practice_keyboard(),
            )
