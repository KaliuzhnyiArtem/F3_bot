from database.start_db import dp_conn, cursor

# test mailing
async def test_maling():
    cursor.execute(f"""SELECT telegram_id FROM users""")
    return cursor.fetchall()