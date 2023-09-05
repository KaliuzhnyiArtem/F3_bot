# Aiogram
from database.workers_dp import get_trainer_tg_id_by_id
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from database.msg_id_history_db import add_message_from_bot
from database.memberships_db import check_client_membership, check_client_membership_for_acces
from database.training_history_db import insert_new_training, insert_new_trial_training
from database.user_db import get_id_trainer_client

# Other
from keybords.menu_buttons import r_back_to_menu, exception_dont_have_abon, dont_has_trainer
from other.calendar_other import get_current_mounth
from other.client_other import acces_choise_data_trainig, type_trening, get_client_id, _check_client_trainer, \
    def_check_start_date
from other.func_other import decorator_check_user, dell_message, callback_ending, ent_in_menu, \
    get_chois_data
from other.help_other import go_left_or_right, training_calendar, hours_inline
from other.membership_othre import check_amount_training, check_amount_trial_training
from other.system import sleep_time


@dp.message_handler(lambda message: message.text == "Обрати день тренування🏋️")
@decorator_check_user
async def show_calendar(message: types.Message, state: FSMContext):

    if await _check_client_trainer(message.from_user.id):
        if await acces_choise_data_trainig(message.from_user.id):

            current_month = await get_current_mounth()

            current_calendar = await training_calendar(numb_month=current_month,
                                                       command='day',
                                                       tg_id=message.from_user.id,
                                                       )

            msg = await message.answer('Оберіть день тренування🏋️', reply_markup=current_calendar)
            await add_message_from_bot(msg)

            msg = await message.answer('.',
                                       reply_markup=r_back_to_menu)
            await add_message_from_bot(msg)

            await state.update_data(last_month=current_month)
        else:
            msg = await message.answer('У вас немає оплаченого абонементу😕\n\n'
                                       'Перейдіть в меню абонементи, та оберіть який вам більше підходить',
                                       reply_markup=exception_dont_have_abon)
            await add_message_from_bot(msg)
    else:
        msg = await message.answer('Ви ще не обрали свого тренера🙁\n\n'
                                   'Перейдіть в меню тренери, та оберіть який вам більше підходить',
                                   reply_markup=dont_has_trainer)
        await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('go-day'))
async def testing_inline(callback: types.CallbackQuery, state: FSMContext):
    tg_client_id = callback.from_user.id
    await go_left_or_right(callback, state, 'day', tg_client_id, "training")


@dp.callback_query_handler(lambda callback: callback.data.startswith('day'))
async def choise_day(callback: types.CallbackQuery, state: FSMContext):

    await state.update_data(choised_day=await callback_ending(callback))
    chois_data = await get_chois_data(state)
    await callback.answer('Дата обрана✅')


    msg = await callback.message.answer(text=f'Оберіть час тренування🏋️',
                                        reply_markup=await hours_inline(callback.from_user.id, chois_data, 'client'))

    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    msg = await callback.message.answer('.',
                                        reply_markup=r_back_to_menu)
    await add_message_from_bot(msg)


@dp.callback_query_handler(lambda callback: callback.data.startswith('hourclient'))
async def choise_hour(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Дата обрана✅')
    await state.update_data(choised_hour=callback.data.split("-")[1])

    training_data = await state.get_data()
    chois_data = await get_chois_data(state)

    id_trainer = await get_id_trainer_client(callback.from_user.id)
    tgid_trainer = await get_trainer_tg_id_by_id(id_trainer[0][0])

    client_id = await get_client_id(callback.from_user.id)

    tp_trainnig = await type_trening(callback.from_user.id)

    if client_id != 0 and id_trainer:
        membership_id = await check_client_membership_for_acces(client_id)

        if tp_trainnig == 'trial':
            await insert_new_trial_training(client_id, id_trainer[0][0], chois_data, training_data['choised_hour'])
            await check_amount_trial_training(client_id)
        elif tp_trainnig == 'training':
            if membership_id:
                await insert_new_training(client_id, id_trainer[0][0],
                                          chois_data, training_data['choised_hour'],
                                          membership_id[0][0])

                await def_check_start_date(membership_id[0][0], chois_data)
                await check_amount_training(callback.from_user.id)

        msg = await callback.message.answer(text=f"Тренування заброньоване ✅\n"
                                                 f"{chois_data}\n"
                                                 f"на {training_data['choised_hour']} ")

        await dell_message(callback.from_user.id)
        await add_message_from_bot(msg)

        msg = await bot.send_message(chat_id=tgid_trainer[0][0], text=f'Назначене нове тренування🥳\n'
                                                                      f'Дата: {chois_data}\n'
                                                                      f"Час: {training_data['choised_hour']}")
        await add_message_from_bot(msg)


    await sleep_time(3)
    await ent_in_menu(callback.from_user.id)




