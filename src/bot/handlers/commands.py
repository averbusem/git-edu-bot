import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import shop_keyboard, start_keyboard
from src.bot.utils.decorators import remove_last_keyboard
from src.db.database import db

router = Router()


@router.message(Command("start"))
@remove_last_keyboard
async def start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    await db.add_new_user(str(message.from_user.id), message.from_user.username)
    await state.clear()
    return await message.answer(f"Привет, {user_name}! Я - твой помощник в изучении Git",
                                reply_markup=start_keyboard())


@router.message(Command("shop"))
async def shop_command(message: Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    all_points = await db.get_all_points(str(user_id))

    await message.answer(f"🛒<b>Магазин</b>\n\n{user_name}, здесь Вы можете приобрести забавные стикеры про git за полученные 🔆")

    photo_num = f"{1}.jpg"

    if await db.is_sticker_owned((str(user_id)), 1):
        photo_path_pattern = os.path.abspath("data/shop/unlocked/")
        photo_path = os.path.join(photo_path_pattern, photo_num)
        # photo_path = "../data/shop/locked/1.jpg"
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, reply_markup=await shop_keyboard(str(user_id), 1))

    else:
        photo_path_pattern = os.path.abspath("data/shop/locked/")
        photo_path = os.path.join(photo_path_pattern, photo_num)
        # photo_path = "../data/shop/unlocked/1.jpg"
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, reply_markup=await shop_keyboard(str(user_id), 1),
                                   caption=f"Стоимость: {settings.STICKER_PRICES[0]}🔆\n\n У вас: {all_points}🔆")
