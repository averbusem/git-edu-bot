import asyncio
import logging

from aiogram.types import BotCommand

from src.bot import bot, dp
from src.db import init_db


async def main():
    await init_db()
    await bot.set_my_commands([BotCommand(command="start", description="Запуск бота"), BotCommand(command="shop", description="Магазин")])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
