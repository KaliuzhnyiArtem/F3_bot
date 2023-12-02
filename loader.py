from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.system_handlers import apsched

storage = MemoryStorage()
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

# Виклик перевірки заморожених обонементів чи не заморожені вони
scheduler.add_job(apsched.check_freez_membership, trigger='cron', hour=23, minute=23, start_date=datetime.now(),
                  kwargs={'bot': bot})

# Виклик перевірки терміну придатності абонементів
scheduler.add_job(apsched.check_timeout_membership, trigger='cron', hour=23, minute=44, start_date=datetime.now(),
                  kwargs={'bot': bot})

scheduler.start()



