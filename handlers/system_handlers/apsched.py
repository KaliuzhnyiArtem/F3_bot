from aiogram import Bot


async def send_message_time(bot: Bot):
    await bot.send_message(1470039104, f"This message do after several time after start bot")


async def send_message_cron(bot: Bot):
    await bot.send_message(1470039104, f"Every day in one time")


async def send_message_interval(bot: Bot, chat_id):
    await bot.send_message(chat_id=chat_id, text=f"Send message with interwals")


async def send_message_cron(bot: Bot):
    await bot.send_message(1470039104, f"Every day in one time")

