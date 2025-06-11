from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import start_keyboard

router = Router()


@router.callback_query(F.data == "main_menu")
async def menu_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    return await callback_query.message.edit_text("📋 <b>Главное меню</b> — выберите раздел:",
                                                  reply_markup=start_keyboard())
