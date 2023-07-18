# Aiogram
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from aiogram import types

#Database
from database.msg_id_history_db import add_message_from_bot

# Other
from other.admin_other import answer_workers_list, update_status_worker, well_done, answer_job_request_list
from other.func_other import decorator_check_admin, dell_message, ent_in_menu_admin
from keybords.admin_menu import r_edit_list_workers, e_edit_workers_info, r_back_to_menu_admin
from other.system import sleep_time


@dp.message_handler(lambda message: message.text == "Редагувати склад персоналу📍")
@decorator_check_admin
async def edit_list_workers(message: types.Message):
    msg = await message.answer("Редагувати склад персоналу📍", reply_markup=r_edit_list_workers)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Звільнення")
@decorator_check_admin
async def edit_list_workers(message: types.Message):

    msg = await message.answer("Оберіть працівника", reply_markup=e_edit_workers_info)
    await add_message_from_bot(msg)
    await answer_workers_list(message, "dismissed")


@dp.callback_query_handler(lambda callback: callback.data.startswith('dismissed'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.data.split('-')[1]

    await callback.answer('Процівника звільнено')

    await update_status_worker(telegram_id=telegram_id, status_id=3)

    msg = await callback.message.answer("Працівника звільнено", reply_markup=r_edit_list_workers)

    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    await well_done(message=callback.message, state=state)


@dp.message_handler(lambda message: message.text == 'Найм нового працівника✅️')
@decorator_check_admin
async def new_worker(message: types.Message):

    msg = await message.answer(text='Тут відображені всі актуальні заявки від нових працівників\n\n'
                               'Для того щоб кандидату відправити заявку, '
                               'йому потрібно написати боту команду /newworker',
                               reply_markup=r_back_to_menu_admin)
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await answer_job_request_list(message)


@dp.callback_query_handler(lambda callback: callback.data.startswith('agree'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.data.split('-')[1]

    await update_status_worker(telegram_id, 2)

    msg = await callback.message.answer("Заявку прийнято✅")
    await dell_message(callback.message.from_user.id)
    await add_message_from_bot(msg)

    await sleep_time(2)
    await ent_in_menu_admin(callback.from_user.id)


@dp.callback_query_handler(lambda callback: callback.data.startswith('refuse'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.data.split('-')[1]

    await update_status_worker(telegram_id, 3)

    msg = await callback.message.answer("Заявку відмовлено✅")
    await dell_message(callback.message.from_user.id)
    await add_message_from_bot(msg)
    await sleep_time(2)

    await ent_in_menu_admin(callback.from_user.id)




