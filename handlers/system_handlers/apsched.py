# from aiogram import Bot
from datetime import datetime
from database.client_membership_db import get_membershiop_id, edit_membership_status
from database.frezz_db import get_all_freez_member, close_last_frezz


async def send_message_time(bot):
    await bot.send_message(1470039104, f"This message do after several time after start bot")


async def send_message_cron(bot):
    """
    Перевірка заморожених абонементів скільки днів вони є замороженими,
    Якщо кількість днів перевищує норму, то абонемент розморожується.
    Та змінюється статус з замороженого на активний
    Args:
        bot:

    Returns:

    """
    # Імпортую тут щоб уникнути циклічного імпортування
    from other.freez_other import day_used
    from database.memberships_db import info_membersips2

    for freez_member_date in await get_all_freez_member():
        used_freez_day = await day_used(freez_member_date[1])

        membership_id = (await get_membershiop_id(freez_member_date[1]))[0][0]

        abot_info = await info_membersips2(membership_id)

        max_used = abot_info[0][1] * 30 // 3

        if used_freez_day > max_used:
            await edit_membership_status(client_abon_id=freez_member_date[1],
                                         status=1)
            await close_last_frezz(freez_member_date[1], datetime.today().date())
            print('Внесені зміни')


async def send_message_interval(bot, chat_id):
    await bot.send_message(chat_id=chat_id, text=f"Send message with interwals")


# async def send_message_cron(bot: Bot):
#     await bot.send_message(1470039104, f"Every day in one time")


async def freez_cheecking(bot, chat_id):
    await bot.send_message(chat_id=1470039104, text=f"Відбулась перевірка заморожених абонементів")

