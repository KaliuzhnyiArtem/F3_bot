from database.memberships_db import dp_conn, cursor


def __check_membership_status():

    cursor.execute('SELECT * FROM membership_satus')
    if not cursor.fetchall():
        __insert_abon_status()


def __check_tainer_status():

    cursor.execute('SELECT * FROM trainer_status')
    if not cursor.fetchall():
        __insert_trainer_status()


def __check_taining_status():

    cursor.execute('SELECT * FROM trainig_status')
    if not cursor.fetchall():
        __insert_training_status()


def insert_all_table_status():

    __check_membership_status()
    __check_tainer_status()
    __check_taining_status()


def __insert_abon_status():
    cursor.execute("""INSERT INTO membership_satus (name) VALUES ('active'), ('frozen'), ('finished')""")
    dp_conn.commit()


def __insert_trainer_status():
    cursor.execute("""INSERT INTO trainer_status (name) 
    VALUES ('active'), ('not active'), ('dissmised'), ('job_request')""")
    dp_conn.commit()


def __insert_training_status():
    cursor.execute("""INSERT INTO trainig_status (name) VALUES ('Planned'), ('Completed'), ('Canceled')""")
    dp_conn.commit()



