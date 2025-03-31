from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import menu_keyboard

router = Router()


@router.callback_query(F.data == "learn_button")
async def learn_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(f"Вы выбрали 'Изучение теории'\n\n"
                                           f"Выберите урок, который хотели бы изучить",
                                           reply_markup=menu_keyboard())
