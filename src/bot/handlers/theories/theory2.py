from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              next_massage_keyboard)
from src.bot.states.theory_states import Theory2State
from src.bot.utils.data_loader import get_theory_data
from src.bot.utils.decorators import clear_last_keyboard

THEORY_DATA = get_theory_data(2)
THEORY_MESSAGES = THEORY_DATA.get("messages", {})


router = Router()


@router.callback_query(F.data == "theory2")
@clear_last_keyboard
async def start_theory2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory2State.MESSAGE2)
    new_message = await callback.message.edit_text(
        THEORY_MESSAGES["message1"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory2State.MESSAGE2)
@clear_last_keyboard
async def theory2_step2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory2State.MESSAGE3)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message2"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory2State.MESSAGE3)
@clear_last_keyboard
async def theory2_step3(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(THEORY_MESSAGES["message3"])
    new_message = await callback.message.answer(
        "Урок завершен! Переходите к тесту или заданию", reply_markup=menu_keyboard()
    )
    return new_message
