from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Back to main menu
from database.workers_dp import get_trainer_telegram_id

r_back_to_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
b_back_menu_admin = KeyboardButton('⏪ Головне меню')
r_back_to_menu_admin.add(b_back_menu_admin)

# Admin menu
r_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_search_clients = KeyboardButton('Пошук по клієнтам🔎')
b_sending_messages = KeyboardButton('Розсилка повідомлень📩')
b_control_workers = KeyboardButton('Управління персоналом👷🏻‍♂️')

r_admin_menu.add(b_search_clients).add(b_sending_messages).add(b_control_workers)

# Menu control management
r_control_workers = ReplyKeyboardMarkup(resize_keyboard=True)
b_edit_list_workers = KeyboardButton("Редагувати склад персоналу📍")
b_edit_workers_info = KeyboardButton("Редагування профілів персоналу📝")
b_weekends_workers = KeyboardButton("Вихідні дні🥳")

r_control_workers.add(b_edit_list_workers).add(b_edit_workers_info).add(b_weekends_workers, b_back_menu_admin)


# Menu edit_list_workers
r_edit_list_workers = ReplyKeyboardMarkup(resize_keyboard=True)
b_add_new_worker = KeyboardButton('Найм нового працівника✅️')
b_dissmis_worker = KeyboardButton('Звільнення')

r_edit_list_workers.add(b_add_new_worker).add(b_dissmis_worker).add(b_back_menu_admin)


# -------------------------------
# Редагування профілів персоналу📝

e_edit_workers_info = ReplyKeyboardMarkup(resize_keyboard=True).add(b_back_menu_admin)


# Menu send email
r_send_email = ReplyKeyboardMarkup(resize_keyboard=True)
b_send_all_client = KeyboardButton('Розсилка повідомлень всім клієнтам')
r_send_email.add(b_send_all_client).add(b_back_menu_admin)

r_ready_text = ReplyKeyboardMarkup(resize_keyboard=True)
b_ready_text = KeyboardButton('Розіслати повідомленння')
r_ready_text.add(b_ready_text).add(b_back_menu_admin)


# Кнопки які використовуються при редагуванні та звільненні працівників
async def generate_chois_worker(telegram_id: int, comand: str):
    """
    При виводі списку працівників
    Метод генерує кнопки до кожного працівника.

    :param telegram_id:
    :param comand:
    :return:
    """
    text = ''
    if comand in ['worker', 'set_week', "dell_week"]:
        text = 'Обрати'
    elif comand == 'dismissed':
        text = 'Звільнити'
    elif comand == 'cgtrainer':
        text = 'Замінити'
    elif comand == 'choisUser':
        text = 'Назначити основним тренером'

    b_chois_worker = InlineKeyboardButton(text=f'{text}', callback_data=f'{comand}-{telegram_id}')
    return InlineKeyboardMarkup().add(b_chois_worker)


async def two_inl_add_diss(telegram_id):
    b_agree_worker = InlineKeyboardButton(text=f'Прийняти', callback_data=f'agree-{telegram_id}')
    b_refuse_worker = InlineKeyboardButton(text=f'Відмовити', callback_data=f'refuse-{telegram_id}')
    return InlineKeyboardMarkup().add(b_agree_worker, b_refuse_worker)



# Menu worker card
r_menu_worker_card = ReplyKeyboardMarkup(resize_keyboard=True)
b_edit_foto = KeyboardButton('Змінити фото📷')
b_edit_name = KeyboardButton('Змінити ФІО📔')
b_edit_description = KeyboardButton('Змінити опис📝')
b_edit_status = KeyboardButton('Змінити статус📊')
r_menu_worker_card.add(b_edit_foto, b_edit_name).add(b_edit_description, b_edit_status).add(b_back_menu_admin)


# change trainer status button
def status_tr(status_now):

    r_change_status = ReplyKeyboardMarkup(resize_keyboard=True)

    if status_now == 1:
        b_action_status = KeyboardButton("Змінити на неактивний👎🏻")
        r_change_status.add(b_action_status)
    elif status_now == 2:
        b_action_status = KeyboardButton("Змінити на активний👍🏻")
        r_change_status.add(b_action_status)

    return r_change_status.add(b_back_menu_admin)


# weekends menu

r_weekend_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_add_weekends = KeyboardButton('Додати вихідний😎')
b_dell_weekends = KeyboardButton('Видалити вихідний😒')
r_weekend_menu.add(b_add_weekends).add(b_dell_weekends).add(b_back_menu_admin)


async def chois_dell_weekend(day):
    b_dell_weekend = InlineKeyboardButton(text='Видалити❌', callback_data=f'dllweek_{day}')
    return InlineKeyboardMarkup().add(b_dell_weekend)
















