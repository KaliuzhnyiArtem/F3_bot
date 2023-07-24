from database.msg_id_history_db import add_message_from_bot
from database.search_client_db import find_client_by_id
from keybords.trainer_menu import r_client_card_for_trainer
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from other.admin_other import get_client_id
from other.client_other import client_info_for_admin
from other.func_other import dell_message
from other.trainer_other import get_name_trainer


@dp.callback_query_handler(lambda callback: callback.data.startswith('trainerclient'))
async def open_client_info(callback: types.CallbackQuery, state: FSMContext):
    tg_id = get_client_id(callback)
    client_info = await find_client_by_id(tg_id)
    client_info = client_info[0]
    trainer_name = await get_name_trainer(client_info[6])

    info = await client_info_for_admin(tg_id, client_info, trainer_name)

    await state.update_data(tg_client_id=tg_id, defoult_tarainer=client_info[6], client_id=client_info[0])

    msg = await callback.message.answer(text=info, reply_markup=r_client_card_for_trainer)

    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)