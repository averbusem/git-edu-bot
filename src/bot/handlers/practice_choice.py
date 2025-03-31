from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import practice_choice_keyboard

router = Router()


@router.callback_query(F.data == "practice_button")
async def practice_choice_button(callback_query: CallbackQuery, state: FSMContext):
    # Выбор типа практики: тест или задание
    await callback_query.message.edit_text(f"Вы выбрали 'Практиковаться'\n\n"
                                           f"Выберите тип практики",
                                           reply_markup=practice_choice_keyboard())
