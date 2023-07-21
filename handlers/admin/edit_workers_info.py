# Aiogram

from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from database.msg_id_history_db import add_message_from_bot
from database.workers_dp import update_worker_description

# Other
from other.admin_other import well_done, get_info_worker, update_foto_worker, convert_corect_text, update_worker_fio, \
    get_status_worker, update_status_worker, answer_workers_list
from other.func_other import decorator_check_admin, dell_message, status_trainer
from keybords.admin_menu import e_edit_workers_info, r_menu_worker_card, r_back_to_menu_admin, \
    status_tr
from state.reg import Card


@dp.message_handler(lambda message: message.text == "Редагування профілів персоналу📝")
@decorator_check_admin
async def edit_list_workers(message: types.Message,):
    msg = await message.answer("Оберіть працівника", reply_markup=e_edit_workers_info)
    await add_message_from_bot(msg)
    await answer_workers_list(message, "worker")


@dp.callback_query_handler(lambda callback: callback.data.startswith('worker'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Картка працівника')
    telegram_id = callback.data.split('-')[1]

    msg = await callback.message.answer(text='.')
    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    trainer_info = await get_info_worker(telegram_id)

    await state.update_data(telegram_worker_id=telegram_id, trainer_photo=trainer_info[0][4])

    if trainer_info[0][4] is not None:
        msg1 = await callback.bot.send_photo(chat_id=callback.from_user.id, photo=trainer_info[0][4])
        await add_message_from_bot(msg1)

    msg = await callback.message.answer(text=f'Картка працівника\n'
                                             f'ФІО: {trainer_info[0][1]} {trainer_info[0][2]}\n\n'
                                             f'Статус: {status_trainer(trainer_info[0][5])}\n\n'
                                             f'Опис: {trainer_info[0][6]}', reply_markup=r_menu_worker_card)

    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Змінити фото📷")
@decorator_check_admin
async def edit_list_workers(message: types.Message):

    msg = await message.answer('Завантажте нове фото', reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)
    await Card.getphoto.set()


@dp.message_handler(content_types=['photo'], state=Card.getphoto)
@decorator_check_admin
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[0]['file_id']
    worker_tg_id = await state.get_data()

    await update_foto_worker(photo_id, worker_tg_id["telegram_worker_id"])

    await well_done(message, state)


@dp.message_handler(lambda message: message.text == "Змінити ФІО📔")
@decorator_check_admin
async def edit_list_workers(message: types.Message):

    msg = await message.answer('Введідть нове Імя та Фамілію наприклад (Іван Стрілець). \n\n'
                               'Якщо плануєте змініти тільки фамілію або імя, всерівно пишіть імя та фамілію',
                               reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)
    await Card.getname.set()


# Отримання та зміна ФІО
@dp.message_handler(state=Card.getname)
@decorator_check_admin
async def edit_list_workers(message: types.Message, state: FSMContext):
    fio = await convert_corect_text(message.text)
    fio = fio.split(' ')

    worker_tg_id = await state.get_data()

    if len(fio) == 2:
        await update_worker_fio(fio[0], fio[1], worker_tg_id["telegram_worker_id"])

        await well_done(message, state)

    else:
        msg = await message.answer(text='🙅‍♂️Некоректний формат вводу\n\n'
                                        'Обовязково вводиться Імя та Фамілія через пробіл',
                                   reply_markup=r_back_to_menu_admin)
        await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Змінити статус📊")
@decorator_check_admin
async def edit_list_workers(message: types.Message, state: FSMContext):
    worker_tg_id = await state.get_data()
    worker_status = await get_status_worker(worker_tg_id["telegram_worker_id"])

    if worker_status[0][0] == 1:
        msg = await message.answer(text='Бажаєте надати тренеру неактивний статус?',
                                   reply_markup=status_tr(worker_status[0][0]))
        await add_message_from_bot(msg)

    elif worker_status[0][0] == 2:
        msg = await message.answer(text='Бажаєте надати тренеру активний статус?',
                                   reply_markup=status_tr(worker_status[0][0]))

        await add_message_from_bot(msg)

    await Card.change_trainer_status.set()


@dp.message_handler(state=Card.change_trainer_status)
@decorator_check_admin
async def edit_tariner_status(message: types.Message, state: FSMContext):
    worker_tg_id = await state.get_data()

    if message.text == 'Змінити на неактивний👎🏻':
        await update_status_worker(worker_tg_id["telegram_worker_id"], 2)
        await well_done(message, state)
    elif message.text == 'Змінити на активний👍🏻':

        if worker_tg_id["trainer_photo"]:
            await update_status_worker(worker_tg_id["telegram_worker_id"], 1)
            await well_done(message, state)
        else:
            msg = await message.answer(text='Не вдалось змінити статус.\n'
                                            'У правцівника відсутня фотографія',
                                       reply_markup=r_back_to_menu_admin)

            await add_message_from_bot(msg)


# Зміна опису тренера
@dp.message_handler(lambda message: message.text == "Змінити опис📝")
@decorator_check_admin
async def edit_description_trainer(message: types.Message):

    msg = await message.answer(text='Відправте одним повідомленням новий текст про тренера',
                               reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)

    await Card.getdescription.set()


@dp.message_handler(lambda message: message.text != "⏪ Головне меню",
                    state=Card.getdescription)
@decorator_check_admin
async def get_new_description(message: types.Message, state: FSMContext):

    worker_tg_id = await state.get_data()
    new_text = await convert_corect_text(message.text)

    try:
        await update_worker_description(worker_tg_id["telegram_worker_id"], new_text)

        await well_done(message, state)
    except:
        msg = await message.answer(text='В тексті присутні спец-символи.\n\n'
                                        'Будь ласка видаліть одинарні, подвійні дужки, косі лінії, крапки з комою',
                                   reply_markup=r_back_to_menu_admin)
        await add_message_from_bot(msg)
