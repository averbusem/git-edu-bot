from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.user_keyboards import (menu_keyboard,
                                              next_massage_keyboard)
from src.bot.states.theory_states import Theory6State
from src.bot.utils.data_loader import get_theory_data
from src.bot.utils.decorators import remove_last_keyboard
from src.db.database import db

THEORY_DATA = get_theory_data(6)
THEORY_MESSAGES = THEORY_DATA.get("messages", {})

router = Router()


@router.callback_query(F.data == "theory6")
async def start_theory6(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    current_activity = await db.get_current_activity(user_id=user_id)
    cur_test = current_activity["test"]
    cur_theory = current_activity["theory"]
    cur_practice = current_activity["practice"]
    if any([cur_theory < 6, cur_test < 6, cur_practice < 6]):
        return await callback.message.edit_text(
            "❗Вы ещё не прошли предыдущий урок\n\n"
            "Возвращайтесь, когда изучите всё в предыдущих уроках",
            reply_markup=menu_keyboard()
        )
    else:
        await state.set_state(Theory6State.MESSAGE2)
        return await callback.message.edit_text(
            THEORY_MESSAGES["message1"],
            reply_markup=next_massage_keyboard()
        )


@router.callback_query(F.data == "next", Theory6State.MESSAGE2)
@remove_last_keyboard
async def theory6_step2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory6State.MESSAGE3)
    return await callback.message.answer(
        THEORY_MESSAGES["message2"],
        reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory6State.MESSAGE3)
@remove_last_keyboard
async def theory6_step3(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory6State.MESSAGE4)
    return await callback.message.answer(
        THEORY_MESSAGES["message3"],
        reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory6State.MESSAGE4)
@remove_last_keyboard
async def theory6_step4(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory6State.MESSAGE5)
    return await callback.message.answer(
        THEORY_MESSAGES["message4"],
        reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory6State.MESSAGE5)
@remove_last_keyboard
async def theory6_step5(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory6State.MESSAGE6)
    return await callback.message.answer(
        THEORY_MESSAGES["message5"],
        reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory6State.MESSAGE6)
@remove_last_keyboard
async def theory6_step6(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Theory6State.MESSAGE7)
    return await callback.message.answer(
        THEORY_MESSAGES["message6"],
        reply_markup=next_massage_keyboard()
    )


@router.callback_query(F.data == "next", Theory6State.MESSAGE7)
@remove_last_keyboard
async def theory6_step7(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(THEORY_MESSAGES["message7"])
    await db.update_current_activity(user_id=str(callback.from_user.id), current_theory=7)
    return await callback.message.answer(
        "Урок завершен! Переходите к тесту или заданию",
        reply_markup=menu_keyboard()
    )
