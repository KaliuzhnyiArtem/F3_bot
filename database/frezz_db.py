from database.start_db import dp_conn, cursor


async def add_new_frezz(id_client_membership, start_date):
    '''
    Додає новий запис в таблицю де зберігається історія заморажування

    :param id_client_membership:
    :param start_date:
    :return:
    '''

    cursor.execute(f'''INSERT INTO frezz (id_client_membership, start_date) 
    VALUES ({id_client_membership}, '{start_date}')''')
    dp_conn.commit()


async def close_last_frezz(id_client_membership, finish_date):
    '''
    Додає дату розморажування абонементу

    :param finish_date:
    :param id_client_membership:
    :return:
    '''
    cursor.execute(f'''UPDATE frezz SET finish_date='{finish_date}'
    WHERE id_client_membership={id_client_membership} and finish_date IS NULL''')

    dp_conn.commit()


async def get_ls_freez_by_id_member(id_client_membership):
    '''
    Отримуємо всю історію заморажування по ід абонементу
    :return:
    '''

    cursor.execute(f"""SELECT start_date, finish_date FROM frezz WHERE id_client_membership={id_client_membership}""")
    return cursor.fetchall()


async def get_all_freez_member():
    """
    Отримуємо список всіх заморожених обенементів,
    без кінцевої дати (заморозка триває ще не завершилась)

    Returns:
    """
    cursor.execute(f"""SELECT * FROM frezz WHERE finish_date IS NULL""")
    return cursor.fetchall()




