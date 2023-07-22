# Aiogram
from datetime import datetime

from aiogram.dispatcher import FSMContext

from database.client_membership_db import edit_membership_status, get_membership_status
from database.frezz_db import add_new_frezz, close_last_frezz
from database.memberships_db import add_to_client_membership, info_membersips2, \
    check_client_membership_active_frozen
from database.search_client_db import find_client_list, find_client_by_id
from database.training_history_db import get_planed_training, dellete_training, get_client_member_id_by_training_id
from keybords.k_search_client import open_profile, r_client_card, r_controll_membership, r_controll_trainings, \
    frezz_on_off, delete_training
from loader import dp, bot
from aiogram import types

# Database
from database.msg_id_history_db import add_message_from_bot

# Other
from other.admin_other import convert_corect_text, get_client_id, well_done
from other.client_other import client_info_for_admin
from other.freez_other import day_used
from other.func_other import decorator_check_admin, dell_message, ent_in_menu_admin, get_data_from_fetchall, \
    get_data_from_fetchall0
from other.membership_othre import count_training_history
from other.system import show_all_memeberships, sleep_time
from other.trainer_other import get_name_trainer
from state.reg import SerachClient
from keybords.admin_menu import r_back_to_menu_admin


@dp.message_handler(lambda message: message.text == 'Пошук по клієнтам🔎')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    await SerachClient.get_client_name.set()
    msg = await message.answer('🔎Для пошуку клієнта введіть імя за яким він був зарегестрований\n\n'
                               'Точне імя можна перевірити в особистому кабінеті клієнта',
                               reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text != '⏪ Головне меню', state=SerachClient.get_client_name)
@decorator_check_admin
async def get_name_client(message: types.Message, state: FSMContext):
    name = await convert_corect_text(message.text)
    client_list = await find_client_list(name)

    if client_list:
        for i in client_list:
            msg = await message.answer(f'Iмя: {i[0]}\n'
                                       f'usernaem: {i[1]}\n'
                                       f'phone: {i[2]}\n', reply_markup=await open_profile(i[3]))

            await add_message_from_bot(msg)

        msg = await message.answer('.', reply_markup=r_back_to_menu_admin)
        await add_message_from_bot(msg)
        await state.finish()
    else:
        msg = await message.answer(f'Такого клієнта не знайдено🙁\n'
                                   f'Спробуйте інше імя', reply_markup=r_back_to_menu_admin)

        await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('client'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):

    tg_id = get_client_id(callback)
    client_info = await find_client_by_id(tg_id)
    client_info = client_info[0]
    trainer_name = await get_name_trainer(client_info[6])

    info = await client_info_for_admin(tg_id, client_info, trainer_name)

    await state.update_data(tg_client_id=tg_id, defoult_tarainer=client_info[6], client_id=client_info[0])

    msg = await callback.message.answer(text=info, reply_markup=r_client_card)

    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Управління абонементом💳')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    msg = await message.answer('Меню управління абонементом💳', reply_markup=r_controll_membership)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Продаж абонементу💳')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    msg = await message.answer('Продаж абонементу💳', reply_markup=r_controll_membership)
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await show_all_memeberships('sellabon', message)
    msg = await message.answer('Оберіть абонемент', reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('sellabon'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):

    msg = await callback.message.answer('Абонемент виданий клієнту✅', reply_markup=r_back_to_menu_admin)
    await dell_message(callback.message.from_user.id)
    await add_message_from_bot(msg)

    await sleep_time(1.5)

    current_data = str(datetime.now().date())
    client_id = (await state.get_data())['client_id']
    id_membersip = int(callback.data.split('-')[1])

    await add_to_client_membership(client_id=client_id, membership_id=id_membersip)

    await ent_in_menu_admin(callback.from_user.id)


@dp.message_handler(lambda message: message.text == 'Заморозка/Розморозка❄️')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    msg = await message.answer('Заморозка/Розморозка❄️', reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)
    client_id = (await state.get_data())['client_id']
    ls_member = await check_client_membership_active_frozen(client_id)

    for client_abon in ls_member:
        abot_info = await info_membersips2(client_abon[2])
        abon_name = abot_info[0][0]

        done_training = await count_training_history(client_abon[0])
        amount_training = f'({done_training}/{abot_info[0][2]})'
        used_freez_day = await day_used(client_abon[0])
        max_used = abot_info[0][1]*30//3

        frezz_stat = f'Використано ❄️ {used_freez_day} з {max_used}'
        if used_freez_day < max_used:
            msg = await message.answer(text=f'{abon_name} - {amount_training}\n\n'
                                            f'{frezz_stat}',
                                       reply_markup=await frezz_on_off(client_abon[4], client_abon[0])
                                       )
        else:

            msg = await message.answer(text=f'{abon_name} - {amount_training}\n\n'
                                            f'{frezz_stat}\n\n'
                                            f'Вичерпаний ліміт заморозки',
                                       )

        await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('freez_on'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):
    membership_id = callback.data.split("-")[1]

    await edit_membership_status(client_abon_id=membership_id,
                                 status=2)
    await add_new_frezz(membership_id, datetime.today().date())
    await well_done(callback.message, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('freez_off'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):
    membership_id = callback.data.split("-")[1]
    print(membership_id)
    await edit_membership_status(client_abon_id=membership_id,
                                 status=1)

    await close_last_frezz(membership_id, datetime.today().date())
    await well_done(callback.message, state)


@dp.message_handler(lambda message: message.text == 'Управління тренуваннями🏋️')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    msg = await message.answer('Меню Управління тренуваннями🏋️', reply_markup=r_controll_trainings)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Видалити тренування🗑')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):

    msg = await message.answer('Оберіть тренування яке бажаете видалити️', reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    client_id = (await state.get_data())['client_id']
    ls_planed_training = await get_planed_training(client_id)
    for training in ls_planed_training:
        msg = await message.answer(f'Дата: {training[3]}\n'
                                   f'Час: {training[4]}', reply_markup=await delete_training(training[0]))
        await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('dell_tr'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):
    training_id = callback.data.split("-")[1]
    id_client_membersip = get_data_from_fetchall(await get_client_member_id_by_training_id(training_id))
    status = get_data_from_fetchall0(await get_membership_status(id_client_membersip))

    await dellete_training(training_id)

    if status == 3:
        await edit_membership_status(id_client_membersip, 1)

    await well_done(callback.message, state)











