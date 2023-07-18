# Aiogram
from database.msg_id_history_db import add_message_from_bot
from database.workers_dp import insert_weekends, delete_weekends
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext


# Other
from other.admin_other import answer_workers_list
from other.calendar_other import get_current_mounth, get_current_year
from other.func_other import decorator_check_admin, dell_message, callback_ending
from keybords.admin_menu import r_back_to_menu_admin, r_weekend_menu
from other.help_other import go_left_or_right, weeked_calendar
from other.weekends_other import answer_weekend_worker


@dp.message_handler(lambda message: message.text == "Вихідні дні🥳")
@decorator_check_admin
async def weekend_hedler(message: types.Message):
    msg = await message.answer('Меню управління вихідними днями🙂', reply_markup=r_weekend_menu)
    await dell_message(message.chat.id)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == "Додати вихідний😎")
@decorator_check_admin
async def weekend_hedler(message: types.Message):
    msg = await message.answer('Оберіть працівника\n'
                               'Якому бажаєте назначити вихідний день', reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)

    await answer_workers_list(message, 'set_week')


# Вивід календаря для вибору вихідного дня
@dp.callback_query_handler(lambda callback: callback.data.startswith('set_week'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    current_month = await get_current_mounth()
    tg_id_worker = await callback_ending(callback)

    await callback.answer(text='Працівник обраний✅')

    current_calendar = await weeked_calendar(numb_month=current_month,
                                             command='week',
                                             tg_id=tg_id_worker)

    msg = await callback.message.answer('Оберіть дату вихідного дня', reply_markup=current_calendar)
    await dell_message(callback.message.chat.id)
    await add_message_from_bot(msg)

    msg = await callback.message.answer('.',
                                        reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)

    await state.update_data(last_month=current_month, tg_id_worker=tg_id_worker)


# Назначення вихідного дня в календарі
@dp.callback_query_handler(lambda callback: callback.data.startswith('week'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer(text='Вихідний назначений✅')

    day = await callback_ending(callback)
    mounth = (await state.get_data('last_month'))['last_month']
    year = await get_current_year()
    tg_id_worker = int((await state.get_data('tg_id_worker'))['tg_id_worker'])

    await insert_weekends(worker_tg_id=tg_id_worker,
                          day=f'{year}-{mounth}-{day}')

    current_calendar = await weeked_calendar(numb_month=mounth,
                                             command='week',
                                             tg_id=tg_id_worker)
    await callback.message.edit_reply_markup(reply_markup=current_calendar)

    msg = await callback.message.answer(f'Вихідний назначений✅\n'
                                        f'На {year}-{mounth}-{day}',
                                        reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)


# Обробляємо натискання кнопки зміни місяця в календарі
@dp.callback_query_handler(lambda callback: callback.data.startswith('go-week'))
async def testing_inline(callback: types.CallbackQuery, state: FSMContext):
    tg_id_worker = int((await state.get_data('tg_id_worker'))['tg_id_worker'])

    await go_left_or_right(callback, state, 'week', tg_id_worker, "weekend")


@dp.message_handler(lambda message: message.text == "Видалити вихідний😒")
@decorator_check_admin
async def weekend_hedler(message: types.Message):

    msg = await message.answer('Оберіть працівника\n'
                               'Якому бажаєте видалити вихідний день', reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)

    await answer_workers_list(message, 'dell_week')
    # await message.answer('dell', reply_markup=r_back_to_menu_admin)
    # await delete_weekends(1470039104, '2023-05-28')


@dp.callback_query_handler(lambda callback: callback.data.startswith('dell_week'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):

    tg_id_worker = await callback_ending(callback)
    await state.update_data(tg_id_worker=tg_id_worker)

    msg = await callback.message.answer("Оберіть вихідний який бажаеєте видалити",
                                        reply_markup=r_back_to_menu_admin)
    await dell_message(callback.message.chat.id)
    await add_message_from_bot(msg)

    await answer_weekend_worker(tg_id_worker, callback)


@dp.callback_query_handler(lambda callback: callback.data.startswith('dllweek'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):

    chois_date = callback.data.split('_')[1]
    tg_id_worker = int((await state.get_data('tg_id_worker'))['tg_id_worker'])

    await delete_weekends(worker_tg_id=tg_id_worker, day=chois_date)
    await callback.answer("Успішно видалено✅")

    msg = await callback.message.answer("Оберіть вихідний який бажаеєте видалити",
                                        reply_markup=r_back_to_menu_admin)
    await dell_message(callback.message.chat.id)
    await add_message_from_bot(msg)
    await answer_weekend_worker(tg_id_worker, callback)

