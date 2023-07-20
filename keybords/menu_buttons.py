from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Back to main menu
from other.client_other import check_show_trial_trainig

r_back_to_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_back_to_menu = KeyboardButton('↩️ Головне меню')
r_back_to_menu.add(b_back_to_menu)


# Button send phone number
reply_get_contact = ReplyKeyboardMarkup(resize_keyboard=True)
get_contact = KeyboardButton("Надіслати контакт", request_contact=True)
reply_get_contact.add(get_contact)


# Main menu
r_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_test_training = KeyboardButton("🏋️Записатись на пробне тренування")
b_cabinet = KeyboardButton('💻Особистий кабінет')
b_abon = KeyboardButton("💳Абонементи")
# b_massage = KeyboardButton("💆‍Масаж")
b_trainer = KeyboardButton('😎Тренери')
b_support = KeyboardButton("🧑‍💻Служба підтримки")
r_menu.add(b_test_training).add(b_cabinet).add(b_abon).add(b_trainer, b_support)


async def main_menu(telegram_id):
    r_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    b_test_training = KeyboardButton("🏋️Записатись на пробне тренування")
    b_cabinet = KeyboardButton('💻Особистий кабінет')
    b_abon = KeyboardButton("💳Абонементи")
    # b_massage = KeyboardButton("💆‍Масаж")
    b_trainer = KeyboardButton('😎Тренери')
    b_support = KeyboardButton("🧑‍💻Служба підтримки")
    if await check_show_trial_trainig(telegram_id):
        r_menu.add(b_test_training)
    r_menu.add(b_cabinet).add(b_abon).add(b_trainer, b_support)
    return r_menu

# Меню коли у він натискає обрати день тренування і внього немає оплаченого абонементу
exception_dont_have_abon = ReplyKeyboardMarkup(resize_keyboard=True).add(b_abon).add(b_back_to_menu)

# Меню коли у у клієнта немає тренера
dont_has_trainer = ReplyKeyboardMarkup(resize_keyboard=True).add(b_trainer).add(b_back_to_menu)
#######
# Suppert Menu
#######
r_supprot = ReplyKeyboardMarkup(resize_keyboard=True)
b_first_treinig = KeyboardButton('Чи є у вас пробне тренування?')
b_fredom_visit = KeyboardButton('Чи є у вас вільне відвідування?')
b_group_treinig = KeyboardButton('Чи є у вас групові тренування')
b_streching = KeyboardButton('Чи є у вас стрейчинг?')
b_time_work = KeyboardButton('Графік роботи')
b_price = KeyboardButton('Ціни')
b_location = KeyboardButton('Де ви знаходитесь?')
b_write_admin = KeyboardButton("Зв'язатися з адміністратором")
b_beck_menu = KeyboardButton('↩️ Головне меню')
r_supprot.add(b_first_treinig).add(b_fredom_visit).add(b_group_treinig).add(b_streching).add(b_location).add(b_time_work, b_price)\
    .add(b_write_admin, b_beck_menu)


# Menu support price
r_price_support = ReplyKeyboardMarkup(resize_keyboard=True).add(b_abon).add(b_beck_menu)

# Menu personal account
r_personal_accont = ReplyKeyboardMarkup(resize_keyboard=True)
b_book_trial_training = KeyboardButton('Обрати дату пробного тренування🏋️')
b_book_training = KeyboardButton('Обрати день тренування🏋️')
# b_book_massage = KeyboardButton('Забронювати дату масажу️💆🏻')
r_personal_accont.add(b_book_training).add(b_back_to_menu)


# Menu booking after paymented trial trainig
r_book_data_training = ReplyKeyboardMarkup(resize_keyboard=True).add(b_book_training).add(b_back_to_menu)


# Inline membership button
async def create_inline_membr(id_member: int, command):
    b_member = InlineKeyboardButton('Обрати', callback_data=f'{command}-{id_member}')
    mrk_membership = InlineKeyboardMarkup().add(b_member)
    return mrk_membership


# Payment button
b_payment = KeyboardButton('Оплатити')
r_payment = ReplyKeyboardMarkup(resize_keyboard=True).add(b_payment).add(b_back_to_menu)


# Chois you work
r_choise_work = ReplyKeyboardMarkup(resize_keyboard=True)
b_choise_trainer = KeyboardButton('Тренер🏋️')
b_chois_massaur = KeyboardButton('Масажист💆🏻')
r_choise_work.add(b_choise_trainer).add(b_back_to_menu)





