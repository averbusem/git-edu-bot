from aiogram import Router


def get_practice_router() -> Router:
    from src.bot.handlers.tasks import task1, tasks_list

    router = Router()
    router.include_router(tasks_list.router)
    router.include_router(task1.router)
    # Подключения роутеров из файлов в handlers/tasks
    return router
