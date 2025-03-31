from aiogram import Router


def get_tests_router() -> Router:
    from src.bot.handlers.tests import tests_list

    router = Router()
    router.include_router(tests_list.router)
    # Подключения роутеров из файлов в handlers/tests
    return router
