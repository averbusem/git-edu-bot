from aiogram import Router


def get_tests_router() -> Router:
    from src.bot.handlers.tests import test1, tests_list

    router = Router()
    router.include_router(tests_list.router)
    router.include_router(test1.router)
    # Подключения роутеров из файлов в handlers/tests
    return router
