
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.db.database import db


def setup_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))

    scheduler.add_job(
        db.reset_day_points_all,  # функция для обнуления
        CronTrigger(hour=0, minute=0),  # каждый день в 00:00
        # IntervalTrigger(minutes=5),
        name="Reset day_points for all users",
        misfire_grace_time=3600  # задача выполнится, даже если бот был недоступен меньше часа
    )

    scheduler.start()
    return scheduler
