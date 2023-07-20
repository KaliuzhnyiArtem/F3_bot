# Aiogram
from database.msg_id_history_db import add_message_history, add_message_from_bot
from database.workers_dp import insert_new_trainer, insert_new_massaur
from keybords.menu_buttons import r_choise_work
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

# Database
from other.admin_other import check_worker, update_status_worker
from other.func_other import decorator_check_trainer, ent_in_menu, dell_message
from other.system import sleep_time
from state.reg import RegWorker



@dp.message_handler(commands=['newworker'])
async def new_worker_menu(message: types.Message, state: FSMContext):
    print('Enterh in new worker')
    await add_message_history(message.from_user.id, message.message_id)


    if await check_worker(message.from_user.id, 4):
        msg = await message.answer(text='Заявка вже подана, очікуйде на рішення😊')
        await dell_message(message.from_user.id)
        await add_message_from_bot(msg)

        await sleep_time(1.5)
        await ent_in_menu(message.from_user.id)
    elif await check_worker(message.from_user.id, 1):
        msg = await message.answer(text='Ви вже працюєте у нас🥳')
        await dell_message(message.from_user.id)
        await add_message_from_bot(msg)

        await sleep_time(2)
        await ent_in_menu(message.from_user.id)

    elif await check_worker(message.from_user.id, 2):
        msg = await message.answer(text='Ви вже працюєте у нас🥳.\n\n'
                                        'Але у вас стоїть неактивний статус\n'
                                        'Адмінінстратор може змінити його на активний')
        await dell_message(message.from_user.id)
        await add_message_from_bot(msg)

        await sleep_time(3)
        await ent_in_menu(message.from_user.id)

    elif await check_worker(message.from_user.id, 3):
        msg = await message.answer(text='Ваша заявка відправлена✅')
        await dell_message(message.from_user.id)
        await add_message_from_bot(msg)
        await update_status_worker(message.from_user.id, 4)

        await sleep_time(1.5)
        await ent_in_menu(message.from_user.id)

    else:
        msg = await message.answer(text='Оберіть посаду', reply_markup=r_choise_work)
        await dell_message(message.from_user.id)
        await add_message_from_bot(msg)
        await RegWorker.choise_work.set()


@dp.message_handler(lambda message: message.text in ['Тренер🏋️', 'Масажист💆🏻'], state=RegWorker.choise_work)
async def trainer_menu(message: types.Message, state: FSMContext):
    await add_message_history(message.from_user.id, message.message_id)

    if message.text == 'Тренер🏋️':
        await insert_new_trainer(name=message.from_user.first_name,
                                 telegram_id=message.from_user.id,
                                 id_trainer_status=4
                                 )
    else:
        await insert_new_massaur(name=message.from_user.first_name,
                                 telegram_id=message.from_user.id,
                                 id_trainer_status=4
                                 )

    msg = await message.answer(text='Ваша заявка відправлена✅')
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)
    await state.finish()

    await sleep_time(1.5)
    await ent_in_menu(message.from_user.id)