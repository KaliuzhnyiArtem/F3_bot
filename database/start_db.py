import psycopg2
from config import host, user, password, db_name


class Startdb:
    def __init__(self):
        try:
            self.dp_conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
            )
            self.cursor = self.dp_conn.cursor()
        except:
            self.cursor.close()

        # Обовязково таблиці статусів перші ініціалізуються
        self.__trainer_statu()
        self.__membership_satus()
        self.__trainig_status()

        self.__create_table_admin()
        self.__create_table_trainer()
        self.__create_table_user()
        self.__create_table_massaer()
        self.__create_table_memberships()

        self.__message_id_history()
        self.__weekends()
        self.__client_membership()
        self.__client_trial_training()
        self.__trainig_history()
        self.__trial_trainig_history()
        self.__frezz_table()

    def get_dp_conn_cursor(self):
        return self.dp_conn, self.cursor

    # Create table users
    def __create_table_user(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        username VARCHAR(50),
        phone VARCHAR(50) NOT NULL,
        telegram_id INT NOT NULL,
        personal_info VARCHAR(1000),
        id_default_trainer INT REFERENCES trainers(trainer_id));""")
        self.dp_conn.commit()

    # Create table membership
    def __create_table_memberships(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS memberships (
        member_id serial PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        price INT NOT NULL,
        activiti_months INT,
        amount_training INT NOT NULL)""")
        self.dp_conn.commit()

    # Crete table admin
    def __create_table_admin(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admin (
        admin_id serial PRIMARY KEY, 
        name VARCHAR(50) NOT NULL, 
        telegram_id INT NOT NULL);""")
        self.dp_conn.commit()

    # Create table trainer
    def __create_table_trainer(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trainers (
        trainer_id serial PRIMARY KEY, 
        name VARCHAR(50) NOT NULL,
        second_name VARCHAR(50) NOT NULL,
        telegram_id INT NOT NULL,
        foto_id VARCHAR(1000),
        id_trainer_status INT DEFAULT 2 REFERENCES trainer_status(status_id),
        description VARCHAR(2000));""")
        self.dp_conn.commit()

    # Create table trainer
    def __create_table_massaer(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS massaer (
        massaer_id serial PRIMARY KEY, 
        name VARCHAR(50) NOT NULL,
        second_name VARCHAR(50) NOT NULL,
        telegram_id INT NOT NULL,
        foto_id VARCHAR(1000),
        id_massaer_status INT DEFAULT 2 REFERENCES trainer_status(status_id),
        description VARCHAR(2000));""")
        self.dp_conn.commit()

    # Create table message_id history
    def __message_id_history(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS message_id_history (
        user_id INT NOT NULL,
        message_id BIGINT
        )""")
        self.dp_conn.commit()

    # Create table trainer_status
    def __trainer_statu(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS trainer_status (
        status_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(50)
        )""")
        self.dp_conn.commit()

    # Create table weekends
    def __weekends(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS weekends (
        weekends_id SERIAL NOT NULL PRIMARY KEY,
        worker_tg_id INT,
        day DATE NOT NULL
        )""")
        self.dp_conn.commit()

    def __client_membership(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS client_membership (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT REFERENCES users(user_id),
        membership_id INT REFERENCES memberships(member_id),
        start_day DATE,
        status_member INT REFERENCES membership_satus(id)
        )""")
        self.dp_conn.commit()

    def __membership_satus(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS membership_satus (
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(50)
        )""")
        self.dp_conn.commit()

    def __trainig_history(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS trainig_history (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES users(user_id),
        trainer_id INT NOT NULL REFERENCES trainers(trainer_id),
        day DATE NOT NULL,
        time_training TIME,
        training_status INT REFERENCES trainig_status(id),
        membership_id INT REFERENCES client_membership(id)
        )""")
        self.dp_conn.commit()

    def __trainig_status(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trainig_status (
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(50)
        )""")
        self.dp_conn.commit()

    def __trial_trainig_history(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS trial_trainig_history (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES users(user_id),
        trainer_id INT NOT NULL REFERENCES trainers(trainer_id),
        day DATE NOT NULL,
        time_training TIME,
        training_status INT REFERENCES trainig_status(id)
        )""")
        self.dp_conn.commit()

    def __massage(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS massage (
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(500),
        time INT,
        price INT,
        comment VARCHAR(50)
        )""")
        self.dp_conn.commit()

    def __massage_history(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS massage_history (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES users(user_id),
        massaer INT NOT NULL REFERENCES massaer(massaer_id),
        day DATE NOT NULL,
        time_training VARCHAR(50),
        training_status INT REFERENCES trainig_status(id)
        )""")
        self.dp_conn.commit()

    def __client_massage(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS client_membership (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT REFERENCES users(user_id),
        massage_id INT REFERENCES massage(id),
        start_day DATE NOT NULL,
        status_member INT REFERENCES membership_satus(id)
        )""")
        self.dp_conn.commit()

    def __client_trial_training(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS client_trial_training (
        id SERIAL NOT NULL PRIMARY KEY,
        client_id INT REFERENCES users(user_id),
        start_day DATE NOT NULL,
        status_member INT REFERENCES membership_satus(id)
        )""")
        self.dp_conn.commit()

    def __frezz_table(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS frezz (
        id SERIAL NOT NULL PRIMARY KEY,
        id_client_membership INT REFERENCES client_membership(id),
        start_date DATE NOT NULL,
        finish_date DATE
        )""")
        self.dp_conn.commit()



dp_conn, cursor = Startdb().get_dp_conn_cursor()



