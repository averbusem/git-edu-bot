import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from src.bot.handlers import get_handlers_router
from src.bot.middlewares.remove_keyboard import RemoveLastKeyboardMiddleware

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.message.middleware(RemoveLastKeyboardMiddleware())
dp.callback_query.middleware(RemoveLastKeyboardMiddleware())
dp.include_router(get_handlers_router())
