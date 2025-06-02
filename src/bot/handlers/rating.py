from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.handlers.keyboards.user_keyboards import (menu_keyboard,
                                                       rating_keyboard)
from src.db.database import db

router = Router()


async def get_user_rankings():
    users = await db.get_all_users()  # Функция возвращает всех пользователей
    sorted_users = sorted(users, key=lambda x: x['day_points'], reverse=True)
    return sorted_users


@router.callback_query(F.data == "rating")
async def rating_button(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    sorted_users = await get_user_rankings()

    if not sorted_users:
        await callback_query.message.edit_text("Рейтинг пуст.", reply_markup=menu_keyboard())
        return

    # Находим пользователя в отсортированном списке
    user_index = next((index for index, user in enumerate(
        sorted_users) if user['_id'] == str(user_id)), None)

    if user_index is None:
        await callback_query.message.edit_text("Пользователь не найден.", reply_markup=menu_keyboard())
        return

    total_users = len(sorted_users)

    # Определяем границы для отображения
    if user_index == 0:
        start_index = 0
        end_index = min(3, total_users)
    elif user_index == total_users - 1:
        start_index = max(0, total_users - 3)
        end_index = total_users
    else:
        start_index = user_index - 1
        end_index = user_index + 2

    # Формируем сообщение с рейтингом
    day_points = await db.get_day_points(user_id)
    ranking_message = f"За сегодня Вы получили: {day_points} 🔆\n\n Рейтинг:\n"
    for index in range(start_index, end_index):
        user = sorted_users[index]
        if index == user_index:
            ranking_message += f"{index + 1}.  <b>{user['username']}</b> - {user['day_points']} 👈\n"
        else:
            ranking_message += f"{index + 1}. {user['username']} - {user['day_points']}\n"

    keyboard = rating_keyboard(start_index, total_users)
    await callback_query.message.edit_text(ranking_message, reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("rating_page:"))
async def change_page(callback_query: CallbackQuery):
    start_index = int(callback_query.data.split(":")[1])
    user_id = callback_query.from_user.id

    sorted_users = await get_user_rankings()
    total_users = len(sorted_users)

    end_index = min(start_index + 3, total_users)

    ranking_message = "Рейтинг:\n\n"
    for index in range(start_index, end_index):
        user = sorted_users[index]
        if user['_id'] == user_id:
            ranking_message += f"{index + 1}. <b>{user['username']}</b> - {user['day_points']} 👈\n"
        else:
            ranking_message += f"{index + 1}. {user['username']} - {user['day_points']}\n"

    keyboard = rating_keyboard(start_index, total_users)
    await callback_query.message.edit_text(ranking_message, reply_markup=keyboard)
