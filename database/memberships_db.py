from database.start_db import dp_conn, cursor


async def insert_new_memberships(name: str, price: int, activiti_months: int, amount_training: int):
    cursor.execute(f"""INSERT INTO memberships 
    (name, price, activiti_months, amount_training) 
    VALUES ('{name}', {price}, {activiti_months}, {amount_training})""")
    dp_conn.commit()


# Return all memberships
async def select_membership():
    cursor.execute(f"""SELECT * FROM memberships ORDER BY member_id DESC""")
    return cursor.fetchall()


# Return info the memberships
async def info_membersips(member_id: int):
    cursor.execute(f"""SELECT * FROM memberships WHERE member_id={member_id}""")
    return cursor.fetchall()[0]


async def info_membersips2(member_id: int):
    cursor.execute(f"""SELECT name, activiti_months, amount_training  FROM memberships WHERE member_id={member_id}""")
    return cursor.fetchall()


async def get_count_training(member_id):
    """
    Повертає кількість тренувань в заданом абонементі
    :param member_id:
    :return:
    """
    cursor.execute(f"""SELECT amount_training FROM memberships WHERE member_id={member_id}""")
    return cursor.fetchall()


async def add_to_client_membership(client_id: int, membership_id: int):
    """
    В таблицю де відображаються абонементи клієнтів, додаємо новий абонемент клієнту

    :param current_data:
    :param client_id:
    :param membership_id:
    :return:
    """
    cursor.execute(f"""INSERT INTO client_membership (client_id, membership_id, status_member) 
    VALUES ({client_id}, {membership_id}, 1)""")
    dp_conn.commit()


async def set_start_date_membership(membership_id, date_start):
    """
    Встановлю дату початку активації абонемента

    :param membership_id:
    :param date_start:
    :return:
    """

    cursor.execute(f"""UPDATE client_membership SET start_day='{date_start}' WHERE id={membership_id}""")
    dp_conn.commit()


async def add_to_trial_training(client_id: int, current_data: str):
    """
    В таблицю де відображаються оплачені пробні тренування клієнтів, додаємо новий абонемент клієнту
    :param client_id:
    :param current_data:
    :return:
    """

    cursor.execute(f"""INSERT INTO client_trial_training (client_id, start_day, status_member) 
    VALUES ({client_id}, '{current_data}', 1)""")
    dp_conn.commit()


async def check_client_trial_training(client_id: int):
    cursor.execute(f"""SELECT * FROM client_trial_training 
    WHERE client_id={client_id} and (status_member=1 or status_member=3)""")
    return cursor.fetchall()


async def check_client_trial_training2(client_id: int):

    cursor.execute(f"""SELECT * FROM client_trial_training 
    WHERE client_id={client_id} and status_member=1""")
    return cursor.fetchall()


async def check_client_membership(client_id):
    cursor.execute(f"""SELECT * FROM client_membership 
    WHERE client_id={client_id} and (status_member=1 or status_member=2)
    ORDER BY id ASC""")
    return cursor.fetchall()


async def check_client_membership_by_idabon(id_client_member):
    cursor.execute(f"""SELECT * FROM client_membership WHERE id={id_client_member} and status_member=1""")
    return cursor.fetchall()



async def check_client_membership_active_frozen(client_id):
    cursor.execute(f"""SELECT * FROM client_membership 
    WHERE client_id={client_id} and (status_member=1 or status_member=2)""")
    return cursor.fetchall()


async def check_client_membership2(client_id):
    """
    Перевіряємо чи був у клієнта колись куплений абоенмент
    Використовуємо для метода check_show_trial_trainig

    Потрібно перевіряти всі статуси, а я забув чи верхній метод десь використовується
    :param client_id:
    :return:
    """
    cursor.execute(f"""SELECT * FROM client_membership WHERE client_id={client_id}""")
    return cursor.fetchall()


async def check_client_trial_history(client_id: int):
    cursor.execute(f"""SELECT * FROM trial_trainig_history WHERE client_id={client_id}""")
    return cursor.fetchall()






