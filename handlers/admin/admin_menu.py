# Aiogram
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types

# Database
from other.func_other import decorator_check_admin, ent_in_menu_admin, dell_message
from database.msg_id_history_db import add_message_from_bot, add_message_history

#Other
from keybords.admin_menu import r_admin_menu, r_control_workers
from state.reg import Card, SerachClient, ClientCard


# Для отримання телеграм ід юзера
@dp.message_handler(commands=['myid'])
async def get_myid(message: types.Message):
    await add_message_history(message.from_user.id, message.message_id)

    msg = await message.answer(text='Ваш персональний id:')
    msg1 = await message.answer(text=message.from_user.id)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)
    await add_message_from_bot(msg1)


# Action to button back to main menu
@dp.message_handler(lambda message: message.text == '⏪ Головне меню')
@decorator_check_admin
async def beck_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await ent_in_menu_admin(message.from_user.id)


# Action to button back to main menu
@dp.message_handler(lambda message: message.text == '⏪ Головне меню',
                    state=[Card.getphoto,
                           Card.getname,
                           Card.change_trainer_status,
                           Card.getdescription,
                           SerachClient,
                           ClientCard,
                           ])
@decorator_check_admin
async def beck_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await ent_in_menu_admin(message.from_user.id)


@dp.message_handler(commands=['admin'])
@decorator_check_admin
async def admin_menu(message: types.Message):
    msg = await message.answer(text='Адмін меню', reply_markup=r_admin_menu)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Управління персоналом👷🏻‍♂️')
@decorator_check_admin
async def control_workers(message: types.Message):
    msg = await message.answer('Управління персоналом👷🏻‍♂️', reply_markup=r_control_workers)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)




