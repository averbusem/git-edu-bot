from aiogram import Router


def get_theory_router() -> Router:
    from src.bot.handlers.theories import theories_list, theory1

    router = Router()
    router.include_router(theories_list.router)
    router.include_router(theory1.router)
    # Подключения роутеров из файлов в handlers/theories
    return router
