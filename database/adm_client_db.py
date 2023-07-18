from database.start_db import dp_conn, cursor


# BLOCK UPDATE CLIENT INFORMATION

# Update name
async def update_name_client(telegram_id: int, name: str):
    cursor.execute(f"""UPDATE users SET first_name=%s WHERE telegram_id={telegram_id}""", (name,))
    dp_conn.commit()


# Update phone
async def update_phone_client(telegram_id: int, phone: str):
    cursor.execute(f"""UPDATE users SET phone=%s WHERE telegram_id={telegram_id}""", (phone,))
    dp_conn.commit()


# Update coment
async def update_personal_info_client(telegram_id: int, personal_info: str):
    cursor.execute(f"""UPDATE users SET personal_info=%s WHERE telegram_id={telegram_id}""", (personal_info,))
    dp_conn.commit()


# Update trainer
async def update_trainer_client(telegram_id: int, trainer_id: str):
    cursor.execute(f"""UPDATE users SET id_default_trainer={trainer_id} WHERE telegram_id={telegram_id}""")
    dp_conn.commit()


# Get trainer_id use telegram_id
async def get_trainer_id(telegram_id: int):
    cursor.execute(f"""SELECT trainer_id FROM trainers WHERE telegram_id={telegram_id}""")
    return cursor.fetchall()


# Get trainer_name use id_trainer
async def get_trainer_name(trainer_id: int):
    cursor.execute(f"""SELECT name, second_name FROM trainers WHERE trainer_id={trainer_id}""")
    return cursor.fetchall()





