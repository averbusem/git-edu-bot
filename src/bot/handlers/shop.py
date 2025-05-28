from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from src.bot.handlers.keyboards.user_keyboards import shop_keyboard

router = Router()


async def send_photo(message: Message, photo_number: int):
    photo_path = f"C:/Users/lenas/git-edu/data/shop/{photo_number}.jpg"
    photo = FSInputFile(photo_path)
    media = InputMediaPhoto(media=photo)
    await message.edit_media(media, reply_markup=shop_keyboard(photo_number))


@router.callback_query(lambda c: c.data.startswith("prev_") or c.data.startswith("next_"))
async def navigate_photos(callback_query: CallbackQuery):
    photo_number = int(callback_query.data.split("_")[1])
    await send_photo(callback_query.message, photo_number)
