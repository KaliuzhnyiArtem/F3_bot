from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

trainers_menu = ReplyKeyboardMarkup(resize_keyboard=True)
serch_client = KeyboardButton(text="Пошук по клієнтам🔍")
training_calendar = KeyboardButton(text='Календар тренувань📆')
trainers_menu.add(serch_client).add(training_calendar)

r_back_to_trainer_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_back_to_trainer_menu = KeyboardButton('🔁Головне меню')
r_back_to_trainer_menu.add(b_back_to_trainer_menu)


r_client_card_for_trainer = ReplyKeyboardMarkup(resize_keyboard=True)
b_add_new_training = KeyboardButton(text='Назначити тренування🥳')
r_client_card_for_trainer.add(b_add_new_training).add(b_back_to_trainer_menu)


async def be_or_not_be(id_training: int, type_training: str):
    b_happen = InlineKeyboardButton(text=f'Відбулось', callback_data=f'happen-{id_training}-{type_training}')
    b_notheppen = InlineKeyboardButton(text=f'Відміна', callback_data=f'notheppen-{id_training}-{type_training}')
    return InlineKeyboardMarkup().add(b_happen, b_notheppen)