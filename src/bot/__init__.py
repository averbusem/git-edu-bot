import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from src.bot.handlers import get_handlers_router
from src.bot.middlewares.update_message_id import UpdateLastMessageIdMiddleware

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.message.middleware(UpdateLastMessageIdMiddleware())
dp.callback_query.middleware(UpdateLastMessageIdMiddleware())
dp.include_router(get_handlers_router())
