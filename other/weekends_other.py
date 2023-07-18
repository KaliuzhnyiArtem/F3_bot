from database.msg_id_history_db import add_message_from_bot
from database.workers_dp import get_weekens_worker
from keybords.admin_menu import chois_dell_weekend
from aiogram import types


async def answer_weekend_worker(tg_id_worker, callback: types.CallbackQuery):
    """
    Виводить в чат список всіх вихідних вказаного працівника по ід

    :param tg_id_worker:
    :param callback:
    :return:
    """
    weekends_list = await get_weekens_worker(tg_id_worker)

    for weekend in weekends_list:

        text = f"Рік: {weekend[0].year}\n" \
               f"Місяць: {weekend[0].month}\n" \
               f"Число: {weekend[0].day}\n"

        msg = await callback.message.answer(text=text,
                                            disable_notification=False,
                                            reply_markup=await chois_dell_weekend(day=str(weekend[0])))
        await add_message_from_bot(msg)

