from database.start_db import dp_conn, cursor


# Check admin
async def check_admin(telegram_id: int) -> bool:
    cursor.execute(f"""SELECT * FROM admin WHERE telegram_id={telegram_id}""")
    if cursor.fetchone():
        return True
    else:
        return False


# Check trainer
async def check_trainer(telegram_id) -> bool:
    cursor.execute(f"""SELECT * FROM trainers WHERE telegram_id={telegram_id}""")
    if cursor.fetchone():
        return True
    else:
        return False


# Check user
async def check_user(telegram_id: int):
    cursor.execute(f"""SELECT * FROM users WHERE telegram_id={telegram_id}""")
    if cursor.fetchone():
        return True
    else:
        return False


# Insert new user
async def insert_new_user(first_name: str, username: str, phone: str, telegram_id: int):
    cursor.execute(f"""INSERT INTO users (first_name, username, phone, telegram_id) 
    VALUES('{first_name}','{username}', '{phone}', {telegram_id});""")
    dp_conn.commit()


# Get id client by telegram_id
async def get_client_id(telegram_id: int):
    cursor.execute(f"""SELECT user_id FROM users WHERE telegram_id={telegram_id}""")

    return cursor.fetchall()


async def get_id_trainer_client(telegram_id: int):
    cursor.execute(f"""SELECT id_default_trainer FROM users WHERE telegram_id={telegram_id}""")

    return cursor.fetchall()


async def add_new_defolt_trainer(telegram_id: int, id_trainer: int):
    cursor.execute(f"""UPDATE users SET id_default_trainer={id_trainer} WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


async def user_list_with_one_trainer(trainer_tg_id):
    """
    Повертає список клєінтів з вказаним дефолтним тренером
    Тренер фільтрується по телеграм ід
    """
    cursor.execute(f"""
    SELECT *
    FROM users
    WHERE id_default_trainer=
        (SELECT trainer_id
         FROM trainers
         WHERE telegram_id={trainer_tg_id});
    """)
    return cursor.fetchall()

