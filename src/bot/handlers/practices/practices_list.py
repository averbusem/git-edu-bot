from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers.keyboards.user_keyboards import practice_list_keyboard

router = Router()


@router.callback_query(F.data == "choice_tasks")
async def tasks_list(callback_query: CallbackQuery, state: FSMContext):
    # Вывод списка заданий
    await callback_query.message.edit_text(
        "Вы выбрали <b>Выполнение заданий 🔧</b>\n\n"
        "Пожалуйста, выберите задание, которое вы хотели бы выполнить",
        reply_markup=practice_list_keyboard()
    )
