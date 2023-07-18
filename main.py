import handlers
from database.system_db import insert_all_table_status
from loader import dp
from aiogram import executor, types
from database.start_db import Startdb

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def on_startup(_):
    Startdb()
    insert_all_table_status()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, timeout=8000)