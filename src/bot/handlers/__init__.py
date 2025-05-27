from aiogram import Router

from src.bot.handlers.theories import theories_list


def get_handlers_router() -> Router:
    from src.bot.handlers import (commands, menu, practice_choice, progress,
                                  rating)
    from src.bot.handlers.practices import get_practice_router
    from src.bot.handlers.tests import get_tests_router
    from src.bot.handlers.theories import get_theory_router

    router = Router()
    router.include_router(commands.router)
    router.include_router(menu.router)
    router.include_router(progress.router)
    router.include_router(rating.router)
    router.include_router(practice_choice.router)
    router.include_router(get_practice_router())
    router.include_router(get_theory_router())
    router.include_router(get_tests_router())

    # Здесь будут остальные подключения роутеров из файлов в handlers
    return router
