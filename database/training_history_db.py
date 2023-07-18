from database.start_db import dp_conn, cursor


async def insert_new_training(client_id, trainer_id, day, time_training, membership_id):
    cursor.execute(f"""INSERT INTO trainig_history 
    (client_id, trainer_id, day, time_training, training_status, membership_id) VALUES 
    ({client_id}, {trainer_id}, '{day}', '{time_training}', 1, {membership_id})""")
    dp_conn.commit()


async def chang_training_status(id_training, training_status):
    cursor.execute(f"""UPDATE trainig_history SET training_status={training_status} WHERE id={id_training}""")
    dp_conn.commit()


async def insert_new_trial_training(client_id, trainer_id, day, time_training):
    cursor.execute(f"""INSERT INTO trial_trainig_history (client_id, trainer_id, day, time_training, training_status) VALUES 
    ({client_id}, {trainer_id}, '{day}', '{time_training}', 1)""")
    dp_conn.commit()


async def amount_training(user_member_id):
    """
    Запрос в бд на отримання кількості тренувань по заданому абонементу клієнта

    :param user_member_id:
    :return:
    """
    cursor.execute(f"""SELECT count(membership_id) FROM trainig_history 
    WHERE membership_id={user_member_id} and (training_status=1 or training_status=2)""")
    return cursor.fetchall()


async def get_planed_training(client_id):
    cursor.execute(f"""SELECT * FROM trainig_history WHERE client_id={client_id} and training_status=1""")
    return cursor.fetchall()


async def get_planed_trial_training(client_id):
    cursor.execute(f"""SELECT * FROM trial_trainig_history WHERE client_id={client_id} and training_status=1""")
    return cursor.fetchall()


async def get_training_by_date(trainer_id: int, day: str):
    """
    Отримуємо список тренувань в заданого тренера по вказаній даті
    :return:
    """

    cursor.execute(f"""SELECT time_training FROM trainig_history WHERE trainer_id={trainer_id} and day='{day}'""")
    return cursor.fetchall()


async def count_trainings_on_times(trainer_id, day):
    cursor.execute(f"""SELECT time_training, count(time_training) FROM trainig_history 
    WHERE trainer_id={trainer_id} and day='{day}'
    GROUP BY day, time_training""")
    return cursor.fetchall()


async def dellete_training(id_training):
    cursor.execute(f"""DELETE FROM trainig_history WHERE id={id_training}""")
    dp_conn.commit()


async def get_client_member_id_by_training_id(training_id):
    cursor.execute(f"""SELECT membership_id FROM trainig_history WHERE id={training_id}""")
    return cursor.fetchall()


async def get_planed_training_for_trainer(trainer_id, cois_day):
    '''
    Повертає всі заплановані тренування , у вказаного тренера та дня
    :return:
    '''
    cursor.execute(f"""SELECT * FROM trainig_history 
    WHERE trainer_id={trainer_id} and training_status=1 and day='{cois_day}'
    ORDER BY time_training""")
    return cursor.fetchall()




