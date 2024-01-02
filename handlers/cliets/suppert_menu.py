# Aiogram
from loader import dp
from aiogram import types

# Database
from database.msg_id_history_db import add_message_from_bot

# Other
from config import href_location
from keybords.menu_buttons import r_back_to_menu, r_price_support
from other.func_other import decorator_check_user


@dp.message_handler(lambda message: message.text == 'Чи є у вас пробне тренування?')
@decorator_check_user
async def location(message: types.Message):
    msg = await message.answer(f"Так звичайно в нас є пробне тренування\n\n"
                               f"📝 На ньому ми з'ясуємо ваші цілі\n\n"
                               f"📍 Обов'язково проговоримо особливості вашого організму\n"
                               f"щоб надалі можна було скласти під нього тренувальний процес💪🏻",
                               reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Чи є у вас вільне відвідування?')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer(f"{message.from_user.first_name}, зараз немає вільного відвідування.\n\n"
                               f"Бо ми спеціалізуємося на персональних тренуваннях\n\n"
                               f"Але якщо ви зацікавлені в тренуваннях з професійним тренером, "
                               f"будь ласка, зв'яжіться з нами, і ми з радістю запропонуємо вам наші пакети послуг😊",
                               reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Чи є у вас групові тренування')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer(f"{message.from_user.first_name}, "
                               f"в даний час ми не пропонуємо групові тренування,\n"
                               f"оскільки спеціалізуємось на персональному підході до кожного клієнта.\n\n"
                               f"Однак, ви можете запросити своїх друзів на тренування та займатися разом з ними😊",
                               reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Графік роботи')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer(f"{message.from_user.first_name}, "
                               f"Ми працюємо за попереднім записом\n\n"
                               f"📝Запис можливий кожного дня\n"
                               f"⌛️з 8:00 до 21:00", reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Ціни')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer(f"{message.from_user.first_name}, "
                               f"ціни на які саме послуги Вас цікавлять?",
                               reply_markup=r_price_support)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Чи є у вас стрейчинг?')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer(f"{message.from_user.first_name}. "
                               f"Всі наші тренування закінчуются заминкою з елементами стретчінгу.\n\n"
                               f"Ви можете попросити тренера зробити довшу заминку💪🏻",
                               reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Де ви знаходитесь?')
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer("Ми знаходимося в центрі Києва 🇺🇦.\n\n"
                               "вул. Микільсько-Ботанічна 3а. \n\n"
                               "В 10-ти хвилинах від м.Університет \n"
                               "В 7-ми хвилинах від м.Площа Льва Толстого \n\n"
                               f'<a href="{href_location}">Маршрут на Google Maps</a>', parse_mode='HTML',
                               reply_markup=r_back_to_menu
                               )
    await add_message_from_bot(msg)

    msg = await message.answer_location(50.437847084679014, 30.505846289005863)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Зв'язатися з адміністратором")
@decorator_check_user
async def location(message: types.Message):

    msg = await message.answer("Для зв'язку з адміністратором\n\n"
                               "Телефонуйте: +380999749915\n\n"

                               "Пишіть в телеграм: @F3fitness", reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Правова інформація')
@decorator_check_user
async def pravova_information(message: types.Message):
    msg1 = await message.answer_document('BQACAgIAAxkBAAJcrGVs29Zjhx0sXpCLKd5nvK6DH5pCAALjRgACVGhoS8fuoLyCO7hGMwQ')
    msg2 = await message.answer_document('BQACAgIAAxkBAAJcE2VrgRzMSmMmGPkmGsG1gS0EMnxSAAKWOwACtfFZS9nc6bs4WasAATME')
    msg3 = await message.answer_document('BQACAgIAAxkBAAJcFGVrgT6e1qTsgbzr7YfxkI1eptEVAAKjOwACtfFZS9UvPjMCJGXhMwQ')
    msg4 = await message.answer_document('BQACAgIAAxkBAAJcHWVrj0HS8wHq4I_rEEGVxHLAKGGBAAIMNQACtfFhS-awc_AQQf-YMwQ', reply_markup=r_back_to_menu)

    await add_message_from_bot(msg1)
    await add_message_from_bot(msg2)
    await add_message_from_bot(msg3)
    await add_message_from_bot(msg4)