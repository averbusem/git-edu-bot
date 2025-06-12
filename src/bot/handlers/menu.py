from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import start_keyboard

router = Router()


@router.callback_query(F.data == "main_menu")
async def menu_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("📋 <b>Главное меню</b> — выберите раздел:",
                                           reply_markup=start_keyboard())


@router.callback_query(F.data == "main_menu_answer")
async def menu_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await callback_query.bot.delete_message(chat_id, message_id)
    await callback_query.bot.delete_message(chat_id, message_id - 1)
    await callback_query.message.answer("📋 <b>Главное меню</b> — выберите раздел:",
                                        reply_markup=start_keyboard())
    await callback_query.answer()
