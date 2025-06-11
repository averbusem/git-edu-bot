from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.bot.handlers import settings
from src.bot.keyboards.user_keyboards import menu_keyboard, rating_keyboard
from src.db.database import db

router = Router()

USERS_PER_PAGE = settings.USERS_PER_PAGE
HALF_PAGE = USERS_PER_PAGE // 2


async def get_user_rankings():
    users = await db.get_all_users()  # Функция возвращает всех пользователей
    sorted_users = sorted(users, key=lambda x: x['day_points'], reverse=True)
    return sorted_users


async def make_ranking_message(start_index, end_index, sorted_users, user_id):
    ranking_message = f"🏆<b>Рейтинг</b> за сегодня\n\n"
    for index in range(start_index, end_index):
        ranking_message += f"{index + 1}. "

        user = sorted_users[index]
        if user['_id'] == user_id:
            ranking_message += f"<b>{user['username']}</b>"
        else:
            ranking_message += f"{user['username']}"

        ranking_message += f" - {user['day_points']}"

        if index == 0:
            ranking_message += "🥇"
        elif index == 1:
            ranking_message += "🥈"
        elif index == 2:
            ranking_message += "🥉"
        elif user['_id'] == user_id:
            ranking_message += "👈"

        ranking_message += "\n"

    return ranking_message


@router.callback_query(F.data == "rating")
async def rating_button(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    sorted_users = await get_user_rankings()

    if not sorted_users:
        await callback_query.message.edit_text("Рейтинг пуст.", reply_markup=menu_keyboard())
        return

    user_index = next((index for index, user in enumerate(
        sorted_users) if user['_id'] == str(user_id)), None)

    if user_index is None:
        await callback_query.message.edit_text("Пользователь не найден.", reply_markup=menu_keyboard())
        return

    total_users = len(sorted_users)

    # Определяем границы отображения
    start_index = max(0, user_index - HALF_PAGE)
    end_index = min(start_index + USERS_PER_PAGE, total_users)

    # Корректируем start_index, если мы в конце списка
    if end_index - start_index < USERS_PER_PAGE:
        start_index = max(0, end_index - USERS_PER_PAGE)

    ranking_message = await make_ranking_message(start_index, end_index, sorted_users, user_id)
    keyboard = rating_keyboard(start_index, total_users)
    await callback_query.message.edit_text(ranking_message, reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("rating_page:"))
async def change_page(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)

    sorted_users = await get_user_rankings()
    total_users = len(sorted_users)

    start_index = int(callback_query.data.split(":")[1])
    end_index = min(start_index + USERS_PER_PAGE, total_users)

    ranking_message = await make_ranking_message(start_index, end_index, sorted_users, user_id)
    keyboard = rating_keyboard(start_index, total_users)
    await callback_query.message.edit_text(ranking_message, reply_markup=keyboard)
