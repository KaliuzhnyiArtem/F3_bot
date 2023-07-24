from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from keybords.admin_menu import b_back_menu_admin

# Генерує інлайн клавіатуру для відкриття профілів клієнтів
async def open_profile(tg_id):
    r_open_profile = InlineKeyboardButton('Відкрити профіль', callback_data=f'client-{tg_id}')
    return InlineKeyboardMarkup().add(r_open_profile)


async def open_profile_for_trainer(tg_id):
    r_open_profile = InlineKeyboardButton('Відкрити профіль', callback_data=f'trainerclient-{tg_id}')
    return InlineKeyboardMarkup().add(r_open_profile)


# Меню при вході картку клієнта
r_client_card = ReplyKeyboardMarkup(resize_keyboard=True)
b_edit_info = KeyboardButton('Редагувати данні клієнта📝')
b_membersip = KeyboardButton('Управління абонементом💳')
b_trainig = KeyboardButton("Управління тренуваннями🏋️")
r_client_card.add(b_edit_info).add(b_membersip).add(b_trainig).add(b_back_menu_admin)


# Menu edit client information
r_edit_client_info = ReplyKeyboardMarkup(resize_keyboard=True)
b_edit_name = KeyboardButton('Імя🎫')
b_edit_phone = KeyboardButton('Телефон📱')
b_defoult_trainer = KeyboardButton('Тренер👍🏻')
b_edit_info = KeyboardButton('Коментар📰')
r_edit_client_info.add(b_edit_name, b_edit_phone).add(b_defoult_trainer, b_edit_info).add(b_back_menu_admin)

r_controll_membership = ReplyKeyboardMarkup(resize_keyboard=True)
b_sell_memberships = KeyboardButton('Продаж абонементу💳')
b_freez = KeyboardButton('Заморозка/Розморозка❄️')


# Клавіатура коли при назначенні тренування у клієнта відсутінй тренер
exeption_havnt_trainer = ReplyKeyboardMarkup(resize_keyboard=True)
exeption_havnt_trainer.add(b_defoult_trainer).add(b_back_menu_admin)

# Клавіатура коли при назначенні тренування у клієнта відсутінй активний абонемент
exeption_havnt_member = ReplyKeyboardMarkup(resize_keyboard=True)
exeption_havnt_member.add(b_sell_memberships).add(b_back_menu_admin)




r_controll_membership.add(b_sell_memberships).add(b_freez).add(b_back_menu_admin)


async def frezz_on_off(status, abonn_id):
    """
    Повертає інлайн клавішу заморозити або розморозити взалежності який статус абонемента
    :param status:
    :param abonn_id:
    :return:
    """
    m_freez = InlineKeyboardMarkup()
    if status == 1:
        return m_freez.add(InlineKeyboardButton(text='Заморозити', callback_data=f'freez_on-{abonn_id}'))
    elif status == 2:
        return m_freez.add(InlineKeyboardButton(text='Розморозити', callback_data=f'freez_off-{abonn_id}'))




r_controll_trainings = ReplyKeyboardMarkup(resize_keyboard=True)
b_add_training = KeyboardButton('Назначити тренування📌')
b_dell_training = KeyboardButton('Видалити тренування🗑')
r_controll_trainings.add(b_add_training).add(b_dell_training).add(b_back_menu_admin)


async def delete_training(training_id):
    m_dell_training = InlineKeyboardMarkup()
    return m_dell_training.add(InlineKeyboardButton(text='Видалити', callback_data=f'dell_tr-{training_id}'))



