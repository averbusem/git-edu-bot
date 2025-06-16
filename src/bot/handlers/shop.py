import os

from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from src.bot.keyboards.user_keyboards import shop_keyboard
from src.bot.utils import settings
from src.db.database import db

router = Router()


async def send_photo(callback_query: CallbackQuery, photo_number: int):
    user_id = callback_query.from_user.id
    photo_num = f"{photo_number}.jpg"
    if await db.is_sticker_owned((str(user_id)), photo_number):
        photo_path_pattern = os.path.abspath("data/shop/unlocked/")
        photo_path = os.path.join(photo_path_pattern, photo_num)
        photo = FSInputFile(photo_path)
        media = InputMediaPhoto(media=photo)
        await callback_query.message.edit_media(media, reply_markup=await shop_keyboard(str(user_id), photo_number))

    else:
        photo_path_pattern = os.path.abspath("data/shop/locked/")
        photo_path = os.path.join(photo_path_pattern, photo_num)
        photo = FSInputFile(photo_path)
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
    sticker_num = f"{sticker_number}.webp"
    sticker_path_pattern = os.path.abspath("data/shop/stickers/")
    sticker_path = os.path.join(sticker_path_pattern, sticker_num)
    await callback_query.message.answer_sticker(sticker=FSInputFile(sticker_path))

    if await db.are_all_stickers_owned(user_id):
        link = settings.STICKER_PACK
        await callback_query.message.answer(
            f'Поздравляем! Вы собрали все стикеры!\n\n Ваш заслуженный <a href="{link}">стикерпак</a> 🎉',
        )

    await callback_query.answer()
