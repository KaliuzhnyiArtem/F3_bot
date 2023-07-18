import datetime

from database.start_db import dp_conn, cursor


# Отримати список тренерів
async def get_trainer_list():
    cursor.execute(f"""SELECT name, second_name, telegram_id, foto_id, description FROM trainers 
    WHERE id_trainer_status<3""")
    return cursor.fetchall()


# Отримати список тренерів тільки з активним статусом
async def get_trainer_list_active():
    cursor.execute(f"""SELECT name, second_name, telegram_id, foto_id, description, trainer_id FROM trainers 
    WHERE id_trainer_status=1""")
    return cursor.fetchall()


# Отримати список масажистів
async def get_massaer_list():
    cursor.execute(f"""SELECT name, second_name, telegram_id FROM massaer WHERE id_massaer_status<3""")
    return cursor.fetchall()


# Отримати список тренерів які відправили заявку на влаштування
async def get_request_trainer_list():
    cursor.execute(f"""SELECT name, second_name, telegram_id FROM trainers WHERE id_trainer_status=4""")
    return cursor.fetchall()


# Отримати список масажистів які відправили заявку на влаштування
async def get_request_massaer_list():
    cursor.execute(f"""SELECT name, second_name, telegram_id FROM massaer WHERE id_massaer_status=4""")
    return cursor.fetchall()


# Отримати telegram id тренерів
async def get_trainer_telegram_id():
    cursor.execute(f"""SELECT telegram_id FROM trainers WHERE id_trainer_status!=3""")
    return cursor.fetchall()


# Отримати данні тренера по id
async def get_trainer_info(telegram_id):
    cursor.execute(f"""SELECT * FROM trainers WHERE telegram_id={telegram_id}""")
    return cursor.fetchall()


# Отримати данні масажиста по id
async def get_masssaer_info(telegram_id):
    cursor.execute(f"""SELECT * FROM massaer WHERE telegram_id={telegram_id}""")
    return cursor.fetchall()


# Змінити фото тренера
async def update_foto_trainer(photo_id: str, telegram_id: int):
    cursor.execute(f"""UPDATE trainers SET foto_id='{photo_id}' WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


# Змінити фото масажиста
async def update_foto_massaur(photo_id: str, telegram_id: int):
    cursor.execute(f"""UPDATE massaer SET foto_id='{photo_id}' WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


# Изменить імя та фамілію тренера
async def update_trainer_fio(name, second_name, telegram_id):
    cursor.execute(f"""UPDATE trainers SET name=%s, second_name=%s WHERE telegram_id={telegram_id}""",
                   (name, second_name,))
    dp_conn.commit()


# Змінити імя та фамілію масажиста
async def update_massaur_fio(name, second_name, telegram_id):
    cursor.execute(f"""UPDATE massaer SET name=%s, second_name=%s WHERE telegram_id={telegram_id}""",
                   (name, second_name,))
    dp_conn.commit()


# Отримуємо актульний статус тренера по ід
async def get_trainer_status(telegram_id) -> list:
    cursor.execute(f"""SELECT id_trainer_status FROM trainers WHERE telegram_id={telegram_id}""")
    return cursor.fetchall()


# Отримуємо актульний статус масажиста по ід
async def get_messaur_status(telegram_id) -> list:
    cursor.execute(f"""SELECT id_massaer_status FROM massaer WHERE telegram_id={telegram_id}""")
    return cursor.fetchall()


# Змінюємо стасут тренера
async def update_trainer_status(telegram_id: int, status_worker):
    cursor.execute(f"""UPDATE trainers SET id_trainer_status={status_worker} WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


# Змінюємо стасут масажиста
async def update_massaur_status(telegram_id: int, status_worker):
    cursor.execute(f"""UPDATE massaer SET id_massaer_status={status_worker} WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


# Зміна опису тренера
async def update_trainer_description(telegram_id: int, description):
    cursor.execute(f"""UPDATE trainers SET description=%s WHERE telegram_id={telegram_id}""", (description,))
    dp_conn.commit()


# Зміна опису тренера
async def update_worker_description(telegram_id: int, description):
    cursor.execute(f"""UPDATE trainers SET description=%s WHERE telegram_id={telegram_id}""", (description,))
    cursor.execute(f"""UPDATE massaer SET description=%s WHERE telegram_id={telegram_id}""", (description,))
    dp_conn.commit()


# Insert new trainer
async def insert_new_trainer(name: str, telegram_id: int, id_trainer_status: int):
    cursor.execute(f"""INSERT INTO trainers (name, second_name, telegram_id, id_trainer_status) 
    VALUES('{name}','. ', {telegram_id}, {id_trainer_status});""")
    dp_conn.commit()


# Insert new massaur
async def insert_new_massaur(name: str, telegram_id: int, id_trainer_status: int):
    cursor.execute(f"""INSERT INTO massaer (name, second_name, telegram_id, id_massaer_status) 
    VALUES('{name}','. ', {telegram_id}, {id_trainer_status});""")
    dp_conn.commit()


# Отримати список тренерів з статусом 4 (заявка вже відправлена)
async def get_trainer_repeat_request(telegram_id: int, status: int):
    cursor.execute(f"""SELECT * FROM trainers WHERE id_trainer_status={status} and telegram_id={telegram_id}""")
    return cursor.fetchall()


# Отримати список масажистів з статусом 4 (заявка вже відправлена)
async def get_massaur_repeat_request(telegram_id: int, status: int):
    cursor.execute(f"""SELECT * FROM trainers WHERE id_trainer_status={status} and telegram_id={telegram_id}""")
    return cursor.fetchall()


# Додавання вихідного дня
async def insert_weekends(worker_tg_id: int, day: str):
    cursor.execute(f"""INSERT INTO weekends (worker_tg_id, day) 
    VALUES({worker_tg_id}, '{day}')""")
    dp_conn.commit()


# Видалення вихідного дня
async def delete_weekends(worker_tg_id: int, day: str):
    cursor.execute(f"""DELETE FROM  weekends WHERE worker_tg_id={worker_tg_id} and day='{day}';""")
    dp_conn.commit()


async def get_weekens_worker(worker_tg_id):
    """
    Повертає всі вихдіні працівника фільтрація по телеграм ід

    :param worker_tg_id:
    :return:
    """
    cursor.execute(f"""SELECT day FROM weekends WHERE worker_tg_id={worker_tg_id}""")
    return cursor.fetchall()


async def get_weekens_worker_by_mounth(worker_tg_id, month):
    """
    Повертає всі вихдіні заданого місяця вказаного працівника

    :param worker_tg_id:
    :param month: (Місяць по якому виконується фільтрація)
    :return:
    """
    cursor.execute(f"""SELECT day FROM weekends 
    WHERE worker_tg_id={worker_tg_id} and extract(month from day) = {month}""")
    return cursor.fetchall()


async def get_day_with_training(worker_id, month, year):
    """
    Повертає список всіх тренувань вказаного тренера в заданом місяці

    :param worker_id:
    :param month:
    :param year:
    :return:
    """

    cursor.execute(f"""SELECT day FROM trainig_history
    WHERE trainer_id={worker_id} and extract(month from day)={month} and extract(year from day)={year} """)
    return cursor.fetchall()


async def get_trainer_full_name(trainer_id):
    cursor.execute(f"""SELECT name, second_name FROM trainers WHERE trainer_id={trainer_id}""")
    return cursor.fetchall()


async def get_trainer_id_by_tg_id(tg_id):
    """
    Отримуємо ід тренера по тг ід
    :param tg_id:
    :return:
    """
    cursor.execute(f"""SELECT trainer_id FROM trainers WHERE telegram_id={tg_id}""")
    return cursor.fetchall()


async def get_trainer_tg_id_by_id(tg_id):
    """
    Отримуємо тг ід тренера по ід
    :param tg_id:
    :return:
    """
    cursor.execute(f"""SELECT telegram_id FROM trainers WHERE trainer_id={tg_id}""")
    return cursor.fetchall()






