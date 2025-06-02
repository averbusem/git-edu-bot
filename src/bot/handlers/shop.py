from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from src.bot.handlers import settings
from src.bot.handlers.keyboards.user_keyboards import shop_keyboard
from src.db.database import db

router = Router()


async def send_photo(callback_query: CallbackQuery, photo_number: int):
    photo_path = f"../data/shop/locked/{photo_number}.jpg"
    photo = FSInputFile(photo_path)
    user_id = callback_query.from_user.id
    all_points = await db.get_all_points(user_id)
    media = InputMediaPhoto(
        media=photo, caption=f"Стоимость: {settings.STICKER_PRICES[photo_number - 1]}🔆\n\n У Вас: {all_points}🔆")
    await callback_query.message.edit_media(media, reply_markup=await shop_keyboard(str(user_id), photo_number))


@router.callback_query(lambda c: c.data.startswith("prev_") or c.data.startswith("next_"))
async def navigate_photos(callback_query: CallbackQuery):
    photo_number = int(callback_query.data.split("_")[1])
    await send_photo(callback_query, photo_number)


@router.callback_query(lambda c: c.data.startswith("buy_"))
async def buy_sticker(callback_query: CallbackQuery):
    sticker_number = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id

    user = await db.users.find_one({"_id": str(user_id)})

    if user is None:
        await callback_query.answer("Пользователь не найден.", show_alert=True)
        return

    price = settings.STICKER_PRICES[sticker_number - 1]
    success = await db.try_spend_points(user_id, price)
    if not success:
        await callback_query.answer("У вас недостаточно 🔆 для покупки этого стикера.", show_alert=True)
        return

    await db.set_sticker_owned(user_id, sticker_number)
    await send_photo(callback_query, sticker_number)
    sticker_path = f"../data/shop/unlocked/{sticker_number}.webp"
    await callback_query.message.answer_sticker(sticker=FSInputFile(sticker_path))

    if await db.are_all_stickers_owned(user_id):
        link = settings.STICKER_PACK
        await callback_query.message.answer(f"Ты собрал все стикеры! Вот ссылка на стикерпак:\n{link}")

    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("show_"))
async def show_sticker(callback_query: CallbackQuery):
    sticker_number = int(callback_query.data.split("_")[1])
    sticker_path = f"../data/shop/unlocked/{sticker_number}.webp"
    await callback_query.message.answer_sticker(sticker=FSInputFile(sticker_path))
    await callback_query.answer()
