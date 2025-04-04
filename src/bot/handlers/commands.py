from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.keyboards.user_keyboards import start_keyboard

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! Я - твой помощник в изучении Git",
                         reply_markup=start_keyboard())
