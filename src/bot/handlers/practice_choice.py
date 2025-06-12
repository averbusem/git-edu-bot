from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import practice_choice_keyboard

router = Router()


@router.callback_query(F.data == "practice_button")
async def practice_choice_button(callback_query: CallbackQuery, state: FSMContext):

    return await callback_query.message.edit_text(
        "Вы выбрали <b>Практиковаться 🚀</b>\n\n"
        "Пожалуйста, выберите тип практики: 📝 тест или 🛠 задание.",
        reply_markup=practice_choice_keyboard()
    )
