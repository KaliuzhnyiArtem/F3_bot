# Aiogram
from database.msg_id_history_db import add_message_history, add_message_from_bot
from database.training_history_db import get_planed_training_for_trainer
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from other.calendar_other import get_current_mounth
from other.func_other import decorator_check_trainer, dell_message, ent_in_menu_trainer, get_chois_data
from keybords.trainer_menu import trainers_menu, r_back_to_trainer_menu
from other.help_other import calendar_for_trainer, go_left_or_right


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
    print('Пошук по клієнтам')


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

    msg = await callback.message.answer(f'Список тренувань', reply_markup=r_back_to_trainer_menu)
    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    await state.update_data(choised_day=callback.data.split("-")[1])

    cois_date = await get_chois_data(state)

    ls_training = await get_planed_training_for_trainer(callback.from_user.id, cois_date)
    print
    if ls_training:
        for training in ls_training:
            msg = await callback.message.answer(training)
            await add_message_from_bot(msg)

    else:
        await callback.message.answer(f'На {cois_date}\n'
                                      f'Немає запланованих тренувань')
        await add_message_from_bot(msg)








