from database.start_db import dp_conn, cursor


# Повертає список клієнтів за вказаним імям
async def find_client_list(name):
    cursor.execute(f"""SELECT first_name, username, phone, telegram_id FROM users WHERE first_name='{name}'""")
    return cursor.fetchall()


# Отримання данних клієнта по ід
async def find_client_by_id(tg_id):
    cursor.execute(f"""SELECT * FROM users WHERE telegram_id={tg_id}""")
    return cursor.fetchall()


async def get_info_client(user_id: int):
    cursor.execute(f"""SELECT * FROM users WHERE user_id={user_id}""")
    return cursor.fetchall()





