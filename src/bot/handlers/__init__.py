from aiogram import Router


def get_handlers_router() -> Router:
    from src.bot.handlers import commands

    router = Router()
    router.include_router(commands.router)
    # Здесь будут остальные подключения роутеров из файлов в handlers
    return router
