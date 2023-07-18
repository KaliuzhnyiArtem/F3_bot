from database.memberships_db import add_to_client_membership, add_to_trial_training
from database.msg_id_history_db import add_message_from_bot
from keybords.menu_buttons import r_book_data_training
from other.func_other import dell_message, get_data_from_fetchall
from database.user_db import get_client_id
from aiogram.dispatcher import FSMContext
from datetime import datetime


async def payment_membersip(message, state: FSMContext):
    """
    Дії які виконуються після оплати абонементу
    :param state:
    :param message:
    :return:
    """
    current_data = str(datetime.now().date())
    client_id = get_data_from_fetchall(await get_client_id(message.from_user.id))
    membership_id = (await state.get_data())['id_membersip']

    await add_to_client_membership(client_id=client_id, membership_id=membership_id)

    msg = await message.answer('Оплата абонементу пройшла успішно✅')
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    msg = await message.answer('Оберіть дату тренування зараз, натиснувши кнопку нижче👇🏻. \n\n'
                               'Також ви можете зробити це пізніше в особистому кабінеті😊',
                               reply_markup=r_book_data_training)
    await add_message_from_bot(msg)


async def payment_massage(message):
    """
    Дії які виконуються після оплати масажу
    :param message:
    :return:
    """
    msg = await message.answer('Оплата масажу успішно✅')
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    msg = await message.answer('Оберіть дату масажу зараз, натиснувши кнопку нижче👇🏻. \n\n'
                               'Також ви можете зробити це пізніше в особистому кабінеті😊',
                               reply_markup=r_book_data_training)
    await add_message_from_bot(msg)


async def payment_trial_trainig(message):
    """
    Дії які виконуються після оплати пробного тренування
    :param message:
    :return:
    """
    current_data = str(datetime.now().date())
    client_id = get_data_from_fetchall(await get_client_id(message.from_user.id))
    await add_to_trial_training(client_id=client_id, current_data=current_data)

    msg = await message.answer('Оплата пробного тренування пройшла успішно✅')
    await dell_message(message.from_user.id)
    await add_message_from_bot(msg)

    msg = await message.answer('Оберіть дату тренування зараз, натиснувши кнопку нижче👇🏻. \n\n'
                               'Також ви можете зробити це пізніше в особистому кабінеті😊',
                               reply_markup=r_book_data_training)
    await add_message_from_bot(msg)
