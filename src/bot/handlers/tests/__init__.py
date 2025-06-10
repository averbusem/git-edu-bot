from aiogram import Router


def get_tests_router() -> Router:
    from src.bot.handlers.tests import (test1, test2, test3, test4, test5, test6,
                                        tests_list)

    router = Router()
    router.include_router(tests_list.router)
    router.include_router(test1.router)
    router.include_router(test2.router)
    router.include_router(test3.router)
    router.include_router(test4.router)
    router.include_router(test5.router)
    router.include_router(test6.router)
    # Подключения роутеров из файлов в handlers/tests
    return router
