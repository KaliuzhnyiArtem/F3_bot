from database.start_db import dp_conn, cursor


# INSERT user_id and message_id in message_id_history
async def add_message_history(user_id: int, message_id: int):
    cursor.execute(f"""INSERT INTO message_id_history (user_id ,message_id) 
    VALUES({user_id}, {message_id})""")
    dp_conn.commit()


# INSERT user_id and message_id in message_id_history (from the bot)
async def add_message_from_bot(msg):
    cursor.execute(f"""INSERT INTO message_id_history (user_id ,message_id) 
    VALUES({msg.chat.id}, {msg.message_id})""")
    dp_conn.commit()


# SELECT message history list
async def get_message_history(user_id: int) -> list:
    with dp_conn:
        with dp_conn.cursor() as curs:
            curs.execute(f"""SELECT message_id FROM message_id_history WHERE user_id={user_id}""")
            return curs.fetchall()


# DELETE message_id from message_history
async def dell_message_id(message_id: int):
    with dp_conn:
        with dp_conn.cursor() as curs:
            curs.execute(f"""DELETE FROM message_id_history WHERE message_id={message_id}""")
            dp_conn.commit()


# amount user message in message_history
async def amount_user_messages(user_id: int) -> int:
    cursor.execute(f"""SELECT count(user_id) FROM message_id_history WHERE user_id={user_id}""")
    return cursor.fetchall()[0][0]
