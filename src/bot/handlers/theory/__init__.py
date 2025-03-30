from aiogram import Router


def get_theory_router() -> Router:
    from src.bot.handlers.theory import theory_list

    router = Router()
    router.include_router(theory_list.router)

    # Подключения роутеров из файлов в handlers/theory
    return router
