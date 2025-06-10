from aiogram import Router


def get_practice_router() -> Router:
    from src.bot.handlers.practices import (practice2, practice3, practice4,
                                            practice5, practices_list)

    router = Router()
    router.include_router(practice2.router)
    router.include_router(practice3.router)
    router.include_router(practice4.router)
    router.include_router(practice5.router)
    router.include_router(practices_list.router)
    # Подключения роутеров из файлов в handlers/practices
    return router
