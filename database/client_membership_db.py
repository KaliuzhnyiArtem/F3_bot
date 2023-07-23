from database.start_db import dp_conn, cursor


async def edit_membership_status(client_abon_id, status: int):
    """
    Функція змінює статус заданого абонемента, вказаного клієнта
    :param client_abon_id:
    :param status:
    :return:
    """
    cursor.execute(f"""UPDATE client_membership SET status_member={status} WHERE id={client_abon_id}""")
    dp_conn.commit()


async def edit_client_trial_status(client_id, status: int):
    """
    Функція змінює статус абонемента пробне тренування, вказаного клієнта
    :param client_abon_id:
    :param status:
    :return:
    """
    cursor.execute(f"""UPDATE client_trial_training SET status_member={status} WHERE client_id={client_id}""")
    dp_conn.commit()


async def get_membershiop_id(client_abon_id: int):
    """
    Повертає ід абонемента, по ід клієнтського абонементу

    :param client_abon_id:
    :return:
    """
    cursor.execute(f"""SELECT membership_id FROM client_membership WHERE id={client_abon_id}""")
    return cursor.fetchall()


async def get_membership_status(client_abon_id):
    """
    Повертає статус абонемента клієнта по ід абонемента
    """
    cursor.execute(f"""SELECT status_member FROM client_membership WHERE id={client_abon_id}""")
    return cursor.fetchall()


async def update_status_if_cancelation(training_id):
    """
    Оновлює статус абонемента клієнта.
    Коли тренер натискає відмінити тренування,
    запрос перевіряє чи активний зараз абонемент до якого належить це тренвання,
    Якщо не активний, то змінює статус на активний(1)
    """
    cursor.execute(f"""
    UPDATE client_membership SET status_member=CASE
        WHEN status_member=3 THEN
        1
        ELSE status_member
        END
    WHERE id= 
        (SELECT id
        FROM client_membership
        WHERE id = 
            (SELECT membership_id
            FROM trainig_history
            WHERE id = {training_id}));
""")
    dp_conn.commit()


async def update_status_trial_if_cancelation(training_id):
    """
    Оновлює статус абонемента пробного треування клієнта.
    Коли тренер натискає відмінити тренування,
    запрос перевіряє чи активний зараз абонемент до якого належить це тренвання,
    Якщо не активний, то змінює статус на активний(1)
    """
    cursor.execute(f"""
    UPDATE client_trial_training SET status_member=CASE
        WHEN status_member=3 THEN
        1
        ELSE status_member
        END
    WHERE client_id= 
        (SELECT client_id 
        FROM trial_trainig_history 
        WHERE id={training_id});
""")
    dp_conn.commit()

