import handlers
from database.system_db import insert_all_table_status
from loader import dp, bot
from aiogram import executor, types
from database.start_db import Startdb

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.system_handlers import apsched
from datetime import datetime, timedelta


async def on_startup(_):
    Startdb()
    insert_all_table_status()

    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    # scheduler.add_job(apsched.send_message_time, trigger='date',
    #                   run_date=datetime.now() + timedelta(seconds=1),
    #                   kwargs={'bot': bot})

    # scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=0.5,
    #                   kwargs={'bot': bot})

    # scheduler.start()
    # scheduler.add_job(apsched.send_message_cron, trigger='cron',
    #                   hour=datetime.now().hour,
    #                   minute=datetime.now().minute+1,
    #                   start_date=datetime.now(), kwargs={'bot':bot})

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, timeout=8000)