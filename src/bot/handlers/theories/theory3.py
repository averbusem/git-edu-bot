from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              next_massage_keyboard)
from src.bot.states.theory_states import Theory3State
from src.bot.utils.data_loader import get_theory_data
from src.bot.utils.decorators import clear_last_keyboard
from src.db.database import db

THEORY_DATA = get_theory_data(3)
THEORY_MESSAGES = THEORY_DATA.get("messages", {})
router = Router()

@router.callback_query(F.data == "theory3")
@clear_last_keyboard
async def start_theory3(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    current_activity = await db.get_current_activity(user_id=user_id)
    cur_test = current_activity["test"]
    cur_theory = current_activity["theory"]
    cur_practice = current_activity["practice"]
    if any([cur_theory < 3, cur_test < 3, cur_practice < 3]):
        await callback.message.edit_text("❗Вы ещё не прошли предыдущий урок\n\n"
                                         "Возвращайтесь, когда изучите всё в предыдущих уроках",
                                         reply_markup=menu_keyboard())
    else:
        await state.set_state(Theory3State.MESSAGE2)
        new_message = await callback.message.edit_text(
            THEORY_MESSAGES["message1"], reply_markup=next_massage_keyboard()
        )
        return new_message


@router.callback_query(F.data == "next", Theory3State.MESSAGE2)
@clear_last_keyboard
async def theory3_step2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory3State.MESSAGE3)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message2"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory3State.MESSAGE3)
@clear_last_keyboard
async def theory3_step3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory3State.MESSAGE4)
    new_message = await callback.message.answer(
        THEORY_MESSAGES["message3"], reply_markup=next_massage_keyboard()
    )
    return new_message


@router.callback_query(F.data == "next", Theory3State.MESSAGE4)
@clear_last_keyboard
async def theory3_step4(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(THEORY_MESSAGES["message4"])
    await db.update_current_activity(user_id=callback.from_user.id, current_theory=4)
    new_message = await callback.message.answer(
        "Урок завершен! Переходите к тесту или заданию", reply_markup=menu_keyboard()
    )
    return new_message