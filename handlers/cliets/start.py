# Aiogram
from datetime import datetime

from database.frezz_db import add_new_frezz, close_last_frezz, get_ls_freez_by_id_member
from database.memberships_db import set_start_date_membership
from database.training_history_db import dellete_training, get_planed_training_for_trainer
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from database.user_db import insert_new_user
from database.msg_id_history_db import add_message_history, add_message_from_bot, amount_user_messages
from database.testing_db import test_maling

# Other
import time

from other.client_other import def_check_start_date
from other.freez_other import delta_day, day_used
from state.reg import Reg, Adm
from handlers.shared import command_list
from other.func_other import ent_in_menu, decorator_check_user


@dp.message_handler(commands=['start'])
@decorator_check_user
async def start(message: types.Message):
    await ent_in_menu(message.from_user.id)


@dp.message_handler(state=Reg.phone, content_types=types.ContentTypes.CONTACT)
async def regusers(message: types.Message, state: FSMContext):

    await add_message_history(user_id=message.from_user.id,
                              message_id=message.message_id)

    await insert_new_user(
        message.from_user.first_name,
        message.chat.username,
        message.contact.phone_number,
        message.from_user.id
    )

    msg = await message.answer('Регестрація пройшла успішно✅')
    await add_message_from_bot(msg)

    time.sleep(1.5)
    await state.finish()

    await ent_in_menu(message.from_user.id)




# Detect unregistered commands
@dp.message_handler(lambda message: message.text not in command_list)
async def one(message: types.Message):
    await add_message_history(user_id=message.from_user.id,
                              message_id=message.message_id)

    amount_msg = await amount_user_messages(message.from_user.id)
    if amount_msg >= 50:
        await ent_in_menu(message.chat.id)


# Testing Group mainlig
@dp.message_handler(state=Adm.group_msg)
async def group_message(message: types.Message, state: FSMContext):
    for i in await test_maling():
        await bot.send_message(i[0], f'{message.text}')
    await state.finish()


#Testing
@dp.message_handler(lambda message: message.text == "1")
async def one(message: types.Message, state: FSMContext):
    ls = await get_planed_training_for_trainer(9, '2023-07-30')
    for i in ls:
        print(i)



@dp.message_handler(lambda message: message.text == "2")
async def two(message: types.Message, state: FSMContext):
    pass







