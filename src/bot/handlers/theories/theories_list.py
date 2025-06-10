from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import theory_list_keyboard

router = Router()


@router.callback_query(F.data == "learn_button")
async def learn_button(callback_query: CallbackQuery, state: FSMContext):
    msg = await callback_query.message.edit_text(
        "<b>📚 Изучение теории</b>\n\n"
        "Выберите урок, который вы хотели бы изучить из списка ниже:",
        reply_markup=theory_list_keyboard(),
    )
    return msg
