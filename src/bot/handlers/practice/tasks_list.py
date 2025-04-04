from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import menu_keyboard

router = Router()


@router.callback_query(F.data == "choice_tasks")
async def tasks_list(callback_query: CallbackQuery, state: FSMContext):
    # Вывод списка заданий
    await callback_query.message.edit_text(
        "<b>Вы выбрали 'Выполнение заданий'! 🔧</b>\n\n"
        "Пожалуйста, выберите задание, которое вы хотели бы выполнить",
        reply_markup=menu_keyboard()
    )
