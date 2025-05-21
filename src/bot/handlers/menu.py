from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers.keyboards.user_keyboards import start_keyboard

router = Router()


@router.callback_query(F.data == "main_menu")
async def manu_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_name = callback_query.from_user.first_name
    await callback_query.message.edit_text(f"Привет, {user_name}! Я - твой помощник в изучении Git",
                                           reply_markup=start_keyboard())
