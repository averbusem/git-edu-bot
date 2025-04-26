from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.user_keyboards import start_keyboard
from src.db.database import db

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    await db.add_new_user(message.from_user.id)
    await state.clear()
    await message.answer(f"Привет, {user_name}! Я - твой помощник в изучении Git",
                         reply_markup=start_keyboard())
