from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

trainers_menu = ReplyKeyboardMarkup(resize_keyboard=True)
serch_client = KeyboardButton(text="Пошук по клієнтам🔍")
training_calendar = KeyboardButton(text='Календар тренувань📆')
trainers_menu.add(serch_client).add(training_calendar)

r_back_to_trainer_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b_back_to_trainer_menu = KeyboardButton('🔁Головне меню')
r_back_to_trainer_menu.add(b_back_to_trainer_menu)