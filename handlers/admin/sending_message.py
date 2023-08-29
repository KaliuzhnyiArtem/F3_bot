# Aiogram
from aiogram.dispatcher import FSMContext

from database.msg_id_history_db import add_message_from_bot
from database.user_db import get_tg_id_all_client
from keybords.admin_menu import r_back_to_menu_admin, r_ready_text
from loader import dp, bot
from aiogram import types

from other.admin_other import convert_corect_text
from other.func_other import decorator_check_admin, ent_in_menu_admin
from other.system import sleep_time
from state.send_main import SendMessage


# Action to button back to main menu
@dp.message_handler(lambda message: message.text == 'Розсилка повідомлень всім клієнтам')
@decorator_check_admin
async def get_text(message: types.Message, state: FSMContext):
    await SendMessage.wait_message_text.set()
    msg = await message.answer('Розсилка повідомлень всім клієнтам\n\n'
                               'Відправте тест для розсилки.\n\n'
                               'Після того як відправите, бот покаже яке повідомлення прийде клієнтам.',
                               reply_markup=r_back_to_menu_admin)
    await add_message_from_bot(msg)
    # адмін вносить текст
    # текст виводиться для перевірки як він буде виглядати у клєінта
    # Після перевірки підтвердження виконується розсилка


@dp.message_handler(state=SendMessage.wait_message_text)
@decorator_check_admin
async def get_text_for_mailing(message: types.Message, state: FSMContext):

    try:
        await SendMessage.text_ready.set()
        mainling_text = await convert_corect_text(message.text)
        msg = await message.answer(text='Надсилаємо приклад яке повідомлення прийде клієнту')
        await add_message_from_bot(msg)
        msg = await message.answer(text=f'{mainling_text}', reply_markup=r_ready_text)
        await add_message_from_bot(msg)

        await state.update_data(mainling_text=f'{message.text}')
    except:
        msg = await message.answer(text='В тексті присутні спец-символи.\n\n'
                                        'Будь ласка видаліть одинарні, подвійні дужки, косі лінії, крапки з комою',
                                   reply_markup=r_back_to_menu_admin)
        await add_message_from_bot(msg)


@dp.message_handler(state=SendMessage.text_ready)
@decorator_check_admin
async def get_text_for_mailing(message: types.Message, state: FSMContext):
    # get list tg id all client
    tg_id_list = await get_tg_id_all_client()
    mailing_text = (await state.get_data())['mainling_text']

    await state.finish()
    for tg_id in tg_id_list:
        try:
            msg = await bot.send_message(chat_id=tg_id[0], text=f"{mailing_text}")
            await add_message_from_bot(msg)
        except:
            pass

    msg = await message.answer('Повідомлення відправлені✅')
    await add_message_from_bot(msg)

    await sleep_time(3)
    await ent_in_menu_admin(message.chat.id)
