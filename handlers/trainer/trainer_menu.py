# Aiogram
from database.client_membership_db import update_status_if_cancelation, update_status_trial_if_cancelation
from database.msg_id_history_db import add_message_history, add_message_from_bot
from database.training_history_db import chang_training_status, chang_trial_training_status
from database.user_db import user_list_with_one_trainer
from keybords.k_search_client import open_profile_for_trainer
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from other.calendar_other import get_current_mounth
from other.func_other import decorator_check_trainer, dell_message, ent_in_menu_trainer, get_chois_data
from keybords.trainer_menu import trainers_menu, r_back_to_trainer_menu, be_or_not_be
from other.help_other import calendar_for_trainer, go_left_or_right
from other.trainer_other import get_traniner_id, info_about_training
from other.trainer_training_other import training_list_for_treiner, cheng_training_status


# Action to button back to main menu
@dp.message_handler(lambda message: message.text == '🔁Головне меню')
@decorator_check_trainer
async def beck_to_main_menu_trainer(message: types.Message, state: FSMContext):
    await state.finish()
    await ent_in_menu_trainer(message.from_user.id)


@dp.message_handler(commands=['trainer'])
@decorator_check_trainer
async def trainer_menu(message: types.Message):
    await add_message_history(message.from_user.id, message.message_id)
    msg = await message.answer(text='Меню Тренера', reply_markup=trainers_menu)
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Пошук по клієнтам🔍" )
@decorator_check_trainer
async def trainer_menu(message: types.Message, state: FSMContext):
    users_list = await user_list_with_one_trainer(message.from_user.id)



    if users_list:
        msg = await message.answer("Оберіть клієнта", reply_markup=r_back_to_trainer_menu)
        await add_message_from_bot(msg)
        for user in users_list:
            msg = await message.answer(f"Ім'я - {user[1]}\n"
                                       f"Телефон - {user[3]}", reply_markup=await open_profile_for_trainer(user[4]))
            await add_message_from_bot(msg)
    else:
        msg = await message.answer("У вас немає жодного клієнта", reply_markup=r_back_to_trainer_menu)
        await add_message_from_bot(msg)






@dp.message_handler(lambda message: message.text == "Календар тренувань📆" )
@decorator_check_trainer
async def trainer_menu(message: types.Message, state: FSMContext):

    current_month = await get_current_mounth()

    current_calendar = await calendar_for_trainer(numb_month=current_month,
                                                  command='trlist')

    msg = await message.answer('Календар тренувань📆\n', reply_markup=r_back_to_trainer_menu)

    await add_message_from_bot(msg)

    msg = await message.answer('Оберіть день для перегляду запланованих тренувань', reply_markup=current_calendar)
    await add_message_from_bot(msg)

    await state.update_data(last_month=current_month)


@dp.callback_query_handler(lambda callback: callback.data.startswith('go-trlist'))
async def testing_inline(callback: types.CallbackQuery, state: FSMContext):
    await go_left_or_right(callback, state, 'trlist', worker_tg_id=None, place="trainer")


@dp.callback_query_handler(lambda callback: callback.data.startswith('trlist'))
async def choise_day(callback: types.CallbackQuery, state: FSMContext):
    """
    Після вибора дати, виводить список всіх запланованих тренувань тренера
    """
    await training_list_for_treiner(callback, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('happen'))
async def happen(callback: types.CallbackQuery, state: FSMContext):
    """
    Якщо натиснута кнопка (Відбулось) статус тренування змінюється на 2 (Завершено)
    """
    id_training = callback.data.split('-')[1]
    type_training = callback.data.split('-')[2]

    await cheng_training_status(type_training, 2, id_training)

    await training_list_for_treiner(callback, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('notheppen'))
async def notheppen(callback: types.CallbackQuery, state: FSMContext):
    """
    Якщо натиснута кнопка (Відміна) статус тренування змінюється на 3 (Відмінено)
    """
    id_training = callback.data.split('-')[1]
    type_training = callback.data.split('-')[2]

    if type_training == 'trial':
        await update_status_trial_if_cancelation(id_training)
    elif type_training == 'ordinary':
        await update_status_if_cancelation(id_training)

    await cheng_training_status(type_training, 3, id_training)

    await training_list_for_treiner(callback, state)








