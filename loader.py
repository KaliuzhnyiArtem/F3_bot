from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API

from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage = MemoryStorage()
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.start()



