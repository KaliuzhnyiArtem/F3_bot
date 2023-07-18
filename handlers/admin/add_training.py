from aiogram.dispatcher import FSMContext

from database.memberships_db import check_client_membership
from database.msg_id_history_db import add_message_from_bot
from database.training_history_db import insert_new_trial_training, insert_new_training
from database.user_db import get_id_trainer_client
from keybords.admin_menu import r_back_to_menu_admin
from keybords.k_search_client import exeption_havnt_member, exeption_havnt_trainer
from keybords.menu_buttons import r_back_to_menu
from loader import dp, bot
from aiogram import types

from other.calendar_other import get_current_mounth
from other.client_other import _check_client_trainer, acces_choise_data_trainig, type_trening, get_client_id
from other.func_other import decorator_check_admin, callback_ending, get_chois_data, dell_message, ent_in_menu_admin
from other.help_other import training_calendar, go_left_or_right, hours_inline
from other.membership_othre import check_amount_trial_training, check_amount_training
from other.system import sleep_time


@dp.message_handler(lambda message: message.text == 'Назначити тренування📌')
@decorator_check_admin
async def serch_client(message: types.Message, state: FSMContext):
    client_id = (await state.get_data())['tg_client_id']

    if await _check_client_trainer(client_id):
        if await acces_choise_data_trainig(client_id):

            current_month = await get_current_mounth()

            current_calendar = await training_calendar(numb_month=current_month,
                                                       command='admday',
                                                       tg_id=client_id,
                                                       )
            msg = await message.answer('Оберіть день тренування🏋️', reply_markup=current_calendar)
            await add_message_from_bot(msg)

            msg = await message.answer('.',
                                       reply_markup=r_back_to_menu_admin)
            await add_message_from_bot(msg)

            await state.update_data(last_month=current_month)
        else:
            msg = await message.answer('У клієнт відсутній активний абонемент\n\n',
                                       reply_markup=exeption_havnt_member)
            await add_message_from_bot(msg)
    else:
        msg = await message.answer('За клієнтом не закріплений тренер\n\n',
                                   reply_markup=exeption_havnt_trainer)
        await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('go-admday'))
async def testing_inline(callback: types.CallbackQuery, state: FSMContext):
    tg_client_id = (await state.get_data())['tg_client_id']
    await go_left_or_right(callback, state, 'admday', tg_client_id, "training")


@dp.callback_query_handler(lambda callback: callback.data.startswith('admday'))
async def choise_day(callback: types.CallbackQuery, state: FSMContext):
    tg_client_id = (await state.get_data())['tg_client_id']
    await state.update_data(choised_day=await callback_ending(callback))
    chois_data = await get_chois_data(state)
    await callback.answer('Дата обрана✅')

    msg = await callback.message.answer(text=f'Оберіть час тренування🏋️',
                                        reply_markup=await hours_inline(tg_client_id, chois_data, place='adm'))

    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    msg = await callback.message.answer('.',
                                        reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('houradm'))
async def choise_hour(callback: types.CallbackQuery, state: FSMContext):
    tg_client_id = (await state.get_data())['tg_client_id']

    await callback.answer('Дата обрана✅')
    await state.update_data(choised_hour=callback.data.split("-")[1])

    training_data = await state.get_data()
    chois_data = await get_chois_data(state)

    id_trainer = await get_id_trainer_client(tg_client_id)
    client_id = await get_client_id(tg_client_id)

    tp_trainnig = await type_trening(tg_client_id)

    if client_id != 0 and id_trainer:
        membership_id = await check_client_membership(client_id)

        if tp_trainnig == 'trial':
            await insert_new_trial_training(client_id, id_trainer[0][0], chois_data, training_data['choised_hour'])
            await check_amount_trial_training(client_id)
        elif tp_trainnig == 'training':
            if membership_id:
                await insert_new_training(client_id, id_trainer[0][0],
                                          chois_data, training_data['choised_hour'],
                                          membership_id[0][0])
                await check_amount_training(tg_client_id)

        msg = await callback.message.answer(text=f"Тренування заброньоване ✅\n"
                                                 f"{chois_data}\n"
                                                 f"на {training_data['choised_hour']} ")

        await dell_message(callback.from_user.id)
        await add_message_from_bot(msg)

    await sleep_time(3)
    await ent_in_menu_admin(callback.from_user.id)
