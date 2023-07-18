
from database.msg_id_history_db import add_message_from_bot
from database.workers_dp import get_trainer_info, get_masssaer_info, update_foto_trainer, update_foto_massaur, \
    update_trainer_fio, update_massaur_fio, get_trainer_status, get_messaur_status, update_trainer_status, \
    update_massaur_status, get_trainer_list, get_massaer_list, get_trainer_repeat_request, get_massaur_repeat_request, \
    get_request_trainer_list, get_request_massaer_list
from keybords.admin_menu import generate_chois_worker, two_inl_add_diss
from other.func_other import ent_in_menu_admin


# Викликаэмо після успішної зміни данних для переходу в головне меню
from other.system import sleep_time


async def well_done(message, state):

    msg = await message.answer(text='Зміни успішно виконанні✅')

    await add_message_from_bot(msg)
    await state.finish()

    await sleep_time(2)
    await ent_in_menu_admin(message.chat.id)


# Отримуємо інформацію про працівника по ід
# (шукаємо в двох таблицях в тренерів та масажистів)
async def get_info_worker(telegram_id):

    trainer_info = await get_trainer_info(telegram_id)
    massaur_info = await get_masssaer_info(telegram_id)

    if not trainer_info and massaur_info:
        return massaur_info
    elif not massaur_info and trainer_info:
        return trainer_info


# Вивід списку тренерів
async def answer_trainer_list(message, command):
    for trainer in await get_trainer_list():
        msg = await message.answer(f"Тренер - {trainer[0]} {trainer[1]}",
                                   reply_markup=await generate_chois_worker(trainer[2], f"{command}"))
        await add_message_from_bot(msg)


# Вивід списку працівників
async def answer_workers_list(message, command):

    await answer_trainer_list(message, command)

    for massaer in await get_massaer_list():
        msg = await message.answer(f"Масажист - {massaer[0]} {massaer[1]}",
                                   reply_markup=await generate_chois_worker(massaer[2], f"{command}"))
        await add_message_from_bot(msg)


# Вивід всіх заявок на влаштування на роботу (робочі в яких статус ==4)
async def answer_job_request_list(message):
    for trainer in await get_request_trainer_list():
        msg = await message.answer(f"Тренер - {trainer[0]}",
                                   reply_markup=await two_inl_add_diss(trainer[2]))
        await add_message_from_bot(msg)

    for massaer in await get_request_massaer_list():
        msg = await message.answer(f"Масажист - {massaer[0]}",
                                   reply_markup=await two_inl_add_diss(massaer[2]))
        await add_message_from_bot(msg)



# Отримуємо статус працівника по ід
# (шукаємо в двох таблицях в тренерів та масажистів)
async def get_status_worker(telegram_id):

    trainer_status = await get_trainer_status(telegram_id)
    massaur_status = await get_messaur_status(telegram_id)

    if not trainer_status and massaur_status:
        return massaur_status
    elif not massaur_status and trainer_status:
        return trainer_status


async def update_status_worker(telegram_id, status_id):
    await update_trainer_status(telegram_id, status_id)
    await update_massaur_status(telegram_id, status_id)


# Обновляємо фото правцівника по тг ід
async def update_foto_worker(photo_id, telegram_id):
    await update_foto_trainer(photo_id, telegram_id)
    await update_foto_massaur(photo_id, telegram_id)


# Обновляємо ФІО правцівника по тг ід
async def update_worker_fio(name, second_name, telegram_id):
    await update_trainer_fio(name, second_name, telegram_id)
    await update_massaur_fio(name, second_name, telegram_id)


# Перевіряє чи є в талиці користувач який раніше подавав запрос
async def check_worker(telegram_id, status):
    if await get_trainer_repeat_request(telegram_id, status) or await get_massaur_repeat_request(telegram_id, status):
        return True
    else:
        return False






async def convert_corect_text(text) -> str:
    return text.replace("'", "\'")


def get_client_id(callback):
    return callback.data.split('-')[1]








