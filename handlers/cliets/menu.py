# Aiogram
from loader import dp, storage, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database

from database.msg_id_history_db import add_message_from_bot

# Other
from keybords.menu_buttons import r_supprot, r_back_to_menu, r_personal_accont
from other.client_other import info_client
from other.func_other import ent_in_menu, decorator_check_user, dell_message


# Action to button back to main menu
from other.system import show_all_memeberships

from other.user_other import show_trainer_list


@dp.message_handler(lambda message: message.text == '↩️ Головне меню')
@decorator_check_user
async def beck_to_main_menu(message: types.Message, state: FSMContext):

    await state.finish()
    await ent_in_menu(message.from_user.id)


@dp.message_handler(lambda message: message.text == '🧑‍💻Служба підтримки')
@decorator_check_user
async def support_service(message: types.Message):

    msg = await message.answer('Оберіть питання яке вас цікавить', reply_markup=r_supprot)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == '💻Особистий кабінет')
@decorator_check_user
async def personal_account(message: types.Message):
    msg = await message.answer('💻Особистий кабінет', reply_markup=r_personal_accont)
    info = await info_client(message)
    msg1 = await message.answer(text=info)
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)
    await add_message_from_bot(msg1)


@dp.message_handler(lambda message: message.text == '💳Абонементи')
@decorator_check_user
async def support_service(message: types.Message):

    await show_all_memeberships('abon', message)

    msg = await message.answer('Оберіть абонемент який найбільше вам подобається😎',
                               reply_markup=r_back_to_menu)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == '😎Тренери')
@decorator_check_user
async def support_service(message: types.Message):
    msg = await message.answer("Оберіть тренера з яким бажаєте займатись😊", reply_markup=r_back_to_menu)
    await add_message_from_bot(msg)

    await show_trainer_list(message)


