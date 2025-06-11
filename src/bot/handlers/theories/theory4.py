from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              next_massage_keyboard)
from src.bot.states.theory_states import Theory4State
from src.bot.utils.data_loader import get_theory_data
from src.bot.utils.decorators import clear_last_keyboard
from src.db.database import db

THEORY_DATA = get_theory_data(4)
THEORY_MESSAGES = THEORY_DATA.get("messages", {})
router = Router()


@router.callback_query(F.data == "theory4")
@clear_last_keyboard
async def start_theory4(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    current_activity = await db.get_current_activity(user_id=user_id)
    cur_test = current_activity["test"]
    cur_theory = current_activity["theory"]
    cur_practice = current_activity["practice"]
    if any([cur_theory < 3, cur_test < 3, cur_practice < 3]):
        await callback.message.edit_text("❗Вы ещё не прошли предыдущий урок\n\n"
                                         "Возвращайтесь, когда изучите всё в предыдущих уроках",
                                         reply_markup=menu_keyboard())
    else:
        await state.set_state(Theory4State.MESSAGE2)
        new_message = await callback.message.edit_text(
            THEORY_MESSAGES["message1"], reply_markup=next_massage_keyboard()
        )
        return new_message


@router.callback_query(F.data == "next", Theory4State.MESSAGE2)
@clear_last_keyboard
async def theory4_step2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory4State.MESSAGE3)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message2"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory4State.MESSAGE3)
@clear_last_keyboard
async def theory4_step3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory4State.MESSAGE4)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message3"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory4State.MESSAGE4)
@clear_last_keyboard
async def theory4_step4(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory4State.MESSAGE5)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message4"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory4State.MESSAGE5)
@clear_last_keyboard
async def theory4_step5(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(THEORY_MESSAGES["message5"])
    user_id = str(callback.from_user.id)
    has_done = (await db.get_current_theory(user_id) > 4)
    await db.update_current_activity(user_id=str(callback.from_user.id), current_theory=5)

    if not has_done:
        await db.update_points(user_id=callback.from_user.id, points=settings.THEORY_POINTS)
        new_message = await callback.message.answer(
            f"Урок завершен! Вы получили {
                settings.THEORY_POINTS} 🔆\n\nПереходите к тесту или заданию.",
            reply_markup=menu_keyboard()
        )
        return new_message
    else:
        new_message = await callback.message.answer(
            f"Урок повторен!\n\nПереходите к тесту или заданию.",
            reply_markup=menu_keyboard()
        )
        return new_message
