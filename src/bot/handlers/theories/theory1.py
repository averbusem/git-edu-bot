from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              next_massage_keyboard)
from src.bot.states.theory_states import Theory1State
from src.bot.utils.data_loader import get_theory_data
from src.bot.utils.decorators import remove_last_keyboard
from src.db.database import db

THEORY_DATA = get_theory_data(1)
THEORY_MESSAGES = THEORY_DATA.get("messages", {})
router = Router()


@router.callback_query(F.data == "theory1")
async def start_theory1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory1State.MESSAGE2)
    return await callback.message.edit_text(
        THEORY_MESSAGES["message1"], reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory1State.MESSAGE2)
@remove_last_keyboard
async def theory1_step2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory1State.MESSAGE3)
    return await callback.message.answer(
        THEORY_MESSAGES["message2"], reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory1State.MESSAGE3)
@remove_last_keyboard
async def theory1_step3(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(THEORY_MESSAGES["message3"])
    user_id = callback.from_user.id
    has_done = (await db.get_current_theory(user_id) > 1)
    await db.update_current_activity(user_id=callback.from_user.id, current_theory=2)

    if not has_done:
        await db.update_points(user_id=callback.from_user.id, points=settings.THEORY_POINTS)
        return callback.message.answer(
            f"Урок завершен! Вы получили {
                settings.THEORY_POINTS} 🔆\n\nПереходите к тесту или заданию.",
            reply_markup=menu_keyboard()
        )
    else:
        return await callback.message.answer(
            f"Урок повторен!\n\nПереходите к тесту или заданию.",
            reply_markup=menu_keyboard()
        )
