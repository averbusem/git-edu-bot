from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import progress_keyboard
from src.db.database import db

router = Router()


@router.callback_query(F.data == "progress_button")
async def learn_button(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    user_info = await db.get_user_statistics(user_id)

    if user_info:
        completed_theories = user_info.get("current_theory", 0) - 1
        completed_tests = user_info.get("current_test", 0) - 1
        completed_practice = user_info.get("current_practice", 0) - 2

        progress_message = (
            f"📈<b>Прогресс</b>\n\n"
            f"Теория: {completed_theories} из {settings.TOTAL_THEORIES}\n"
            f"Тесты: {completed_tests} из {settings.TOTAL_TESTS}\n"
            f"Практика: {completed_practice} из {settings.TOTAL_PRACTICES}\n\n"
        )
    else:
        progress_message = "Не удалось получить информацию о прогрессе."

    await callback_query.message.edit_text(progress_message, reply_markup=progress_keyboard())
