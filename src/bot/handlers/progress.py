from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import menu_keyboard

router = Router()


@router.callback_query(F.data == "progress_button")
async def learn_button(callback_query: CallbackQuery):
    # Вывод прогресса пользователя
    await callback_query.message.edit_text(f"Вы выбрали 'Прогресс'\n\n"
                                           f"Имя: {callback_query.from_user.first_name}",
                                           reply_markup=menu_keyboard())
