# Aiogram
from aiogram.dispatcher import FSMContext

from database.adm_client_db import update_name_client, update_personal_info_client, update_phone_client, \
    update_trainer_client, get_trainer_id
from loader import dp, bot
from aiogram import types

# Database
from database.msg_id_history_db import add_message_from_bot

# Other
from other.admin_other import convert_corect_text, well_done, answer_trainer_list, get_client_id
from other.func_other import decorator_check_admin, dell_message
from keybords.k_search_client import r_edit_client_info
from keybords.admin_menu import r_back_to_menu_admin
from state.reg import ClientCard


@dp.message_handler(lambda message: message.text == 'Редагувати данні клієнта📝')
@decorator_check_admin
async def ed_client_info(message: types.Message):
    msg = await message.answer('В цьому меню ви можете змінити данні клієнта😊 \n\n'
                               'Оберіть що саме бажаєте редагувати', reply_markup=r_edit_client_info)
    await add_message_from_bot(msg)


@dp.message_handler(lambda message: message.text == 'Імя🎫')
@decorator_check_admin
async def ed_client_name(message: types.Message, state: FSMContext):
    msg = await message.answer(text=f"Введіть нове імя клієнта", reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await ClientCard.edit_name.set()


@dp.message_handler(lambda message: message.text != "⏪ Головне меню", state=ClientCard.edit_name)
@decorator_check_admin
async def get_new_name(message: types.Message, state: FSMContext):
    checked_text = await convert_corect_text(message.text)
    tg_id_client = await state.get_data()
    tg_id_client = tg_id_client['tg_client_id']

    await update_name_client(tg_id_client, checked_text)

    await well_done(message=message, state=state)


@dp.message_handler(lambda message: message.text == 'Коментар📰')
@decorator_check_admin
async def ed_client_comment(message: types.Message, state: FSMContext):
    msg = await message.answer(text=f"Введіть новий коментар для клієнта", reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await ClientCard.edit_commet.set()


@dp.message_handler(lambda message: message.text != "⏪ Головне меню", state=ClientCard.edit_commet)
@decorator_check_admin
async def get_new_comment(message: types.Message, state: FSMContext):

    checked_text = await convert_corect_text(message.text)
    tg_id_client = await state.get_data()
    tg_id_client = tg_id_client['tg_client_id']

    await update_personal_info_client(tg_id_client, checked_text)
    await well_done(message=message, state=state)


@dp.message_handler(lambda message: message.text == 'Телефон📱')
@decorator_check_admin
async def ed_client_phone(message: types.Message, state: FSMContext):
    msg = await message.answer(text=f"Введіть новий телефон клієнта\n\n"
                                    f"Вводьте тільки цифри без додаткових знаків: +:- итд.",
                               reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await ClientCard.edit_phone.set()


@dp.message_handler(lambda message: message.text != "⏪ Головне меню", state=ClientCard.edit_phone)
@decorator_check_admin
async def get_new_phone(message: types.Message, state: FSMContext):
    checked_text = await convert_corect_text(message.text)
    tg_id_client = await state.get_data()
    tg_id_client = tg_id_client['tg_client_id']

    await update_phone_client(tg_id_client, checked_text)
    await well_done(message=message, state=state)


@dp.message_handler(lambda message: message.text == 'Тренер👍🏻')
@decorator_check_admin
async def ed_client_trainer(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    id_defoult_trainer = state_data['defoult_tarainer']

    msg = await message.answer(text=f"Оберіть тренера з запропонованих", reply_markup=r_back_to_menu_admin)

    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    await answer_trainer_list(message, 'cgtrainer')


@dp.callback_query_handler(lambda callback: callback.data.startswith('cgtrainer'))
async def edit_defoult_trainer(callback: types.CallbackQuery, state: FSMContext):

    tg_trainer_id = get_client_id(callback)
    tg_id_client = (await state.get_data())['tg_client_id']

    id_trainer = (await get_trainer_id(tg_trainer_id))[0][0]

    await callback.answer('Тренера змінено✅')

    await update_trainer_client(telegram_id=tg_id_client,
                                trainer_id=id_trainer)

    await well_done(callback.message, state)



