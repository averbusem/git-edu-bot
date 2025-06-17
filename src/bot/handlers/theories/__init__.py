from aiogram import Router


def get_theory_router() -> Router:
    from src.bot.handlers.theories import (theories_list, theory1, theory2,
                                           theory3, theory4, theory5, theory6, theory7)

    router = Router()
    router.include_router(theories_list.router)
    router.include_router(theory1.router)
    router.include_router(theory2.router)
    router.include_router(theory3.router)
    router.include_router(theory4.router)
    router.include_router(theory5.router)
    router.include_router(theory6.router)
    router.include_router(theory7.router)    
    # Подключения роутеров из файлов в handlers/theories
    return router
