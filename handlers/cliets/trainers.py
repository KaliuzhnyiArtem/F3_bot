# Aiogram
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram import types

# Database
from database.user_db import add_new_defolt_trainer


# Other
from other.func_other import well_done_client


@dp.callback_query_handler(lambda callback: callback.data.startswith('choisUser'))
async def chois_worker(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✅Тренер обраний")

    id_trainer = int(callback.data.split('-')[1])

    await add_new_defolt_trainer(telegram_id=callback.from_user.id,
                                 id_trainer=id_trainer)

    await well_done_client(callback.message, state)
