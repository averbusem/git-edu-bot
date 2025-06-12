from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import tests_list_keyboard

router = Router()


@router.callback_query(F.data == "choice_tests")
async def tests_list(callback_query: CallbackQuery, state: FSMContext):
    # Вывод списка тестов
    return await callback_query.message.edit_text(
        "Вы выбрали <b>Решение тестов 🎯</b>\n\n"
        "Пожалуйста, выберите тест, который вы хотели бы пройти",
        reply_markup=tests_list_keyboard()
    )
