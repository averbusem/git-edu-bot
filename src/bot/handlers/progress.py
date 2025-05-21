from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.handlers.keyboards.user_keyboards import menu_keyboard
from src.db.database import db

router = Router()


@router.callback_query(F.data == "progress_button")
async def learn_button(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    user_info = await db.get_user_statistics(user_id)

    if user_info:
        completed_theories = user_info.get("current_theory", 0) - 1
        completed_tests = user_info.get("current_test", 0) - 1
        completed_practice = user_info.get("current_practice", 0) - 1
        all_points = user_info.get("all_points", 0)
        day_points = user_info.get("day_points", 0)

        progress_message = (
            f"Вы выбрали 'Прогресс'\n\n"
            f"Имя: {callback_query.from_user.first_name}\n\n"
            f"Теория: {completed_theories} из {settings.TOTAL_THEORIES}\n"
            f"Тесты: {completed_tests} из {settings.TOTAL_TESTS}\n"
            f"Практика: {completed_practice} из {settings.TOTAL_PRACTICES}\n\n"
            f"Суммарный опыт: {all_points}\n"
            f"Опыт за сегодня: {day_points}"
        )
    else:
        progress_message = "Не удалось получить информацию о прогрессе."

    await callback_query.message.edit_text(progress_message, reply_markup=menu_keyboard())
