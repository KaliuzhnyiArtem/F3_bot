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


# scheduler.add_job(apsched.freez_cheecking, trigger='interval', seconds=1.5,
#                   kwargs={'bot': bot, 'chat_id': 1470039104})

# Виклик перевірки заморожених обонементів чи не заморожені вони
scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=2, minute=2, start_date=datetime.now(),
                  kwargs={'bot': bot})
scheduler.start()



