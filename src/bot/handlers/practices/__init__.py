from aiogram import Router


def get_practice_router() -> Router:
    from src.bot.handlers.practices import practice1, practices_list

    router = Router()
    router.include_router(practice1.router)
    router.include_router(practices_list.router)
    # Подключения роутеров из файлов в handlers/practices
    return router
