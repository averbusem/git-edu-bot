from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from src.bot.handlers.keyboards.user_keyboards import (shop_keyboard,
                                                       start_keyboard)
from src.db.database import db

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    await db.add_new_user(message.from_user.id, message.from_user.username)
    await state.clear()
    await message.answer(f"Привет, {user_name}! Я - твой помощник в изучении Git",
                         reply_markup=start_keyboard())


@router.message(Command("shop"))
async def shop_command(message: Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"{user_name}, вперед за покупками!\n\nЗдесь Вы можете приобрести забавные стикеры за полученный опыт. По стрелкам можно посмотреть все товары.")

    photo_path = "C:/Users/lenas/git-edu/data/shop/1.jpg"
    photo = FSInputFile(photo_path)

    await message.answer_photo(photo=photo, reply_markup=shop_keyboard(1))
