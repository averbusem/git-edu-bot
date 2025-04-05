from aiogram import Router


def get_practice_router() -> Router:
    from src.bot.handlers.tasks import tasks_list

    router = Router()
    router.include_router(tasks_list.router)
    # Подключения роутеров из файлов в handlers/tasks
    return router
