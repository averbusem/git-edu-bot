from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import menu_keyboard

router = Router()


@router.callback_query(F.data == "choice_tests")
async def tests_list(callback_query: CallbackQuery, state: FSMContext):
    # Вывод списка тестов
    await callback_query.message.edit_text(f"Вы выбрали 'Решение тестов' в качестве практики\n\n"
                                           f"Выберите тест, который хотели бы пройти",
                                           reply_markup=menu_keyboard())
