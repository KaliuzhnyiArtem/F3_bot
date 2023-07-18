# Aiogram
from keybords.trainer_menu import trainers_menu
from loader import bot
from aiogram import types

# Database
from database.msg_id_history_db import get_message_history, dell_message_id, \
    add_message_history, add_message_from_bot
from database.user_db import check_user, check_admin, check_trainer

# Other
from keybords.menu_buttons import reply_get_contact, main_menu
from keybords.admin_menu import r_admin_menu
from other.calendar_other import get_current_year
from other.system import sleep_time
from state.reg import Reg



async def ent_in_menu(chat_id: int):
    msg = await bot.send_message(chat_id=chat_id, text='Ви в головному меню', reply_markup=await main_menu(chat_id))
    await dell_message(chat_id=chat_id)
    await add_message_history(user_id=chat_id, message_id=msg.message_id)


async def ent_in_menu_admin(chat_id: int):
    msg = await bot.send_message(chat_id=chat_id, text='Адмін меню', reply_markup=r_admin_menu)

    await dell_message(chat_id=chat_id)

    await add_message_history(user_id=chat_id, message_id=msg.message_id)


async def ent_in_menu_trainer(chat_id: int):
    msg = await bot.send_message(chat_id=chat_id, text='Меню Тренера', reply_markup=trainers_menu)
    await dell_message(chat_id)
    await add_message_from_bot(msg)


async def dell_message(chat_id: int):
    msg_history = await get_message_history(chat_id)
    for i in msg_history:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=i[0])
            await dell_message_id(i[0])
        except:
            await dell_message_id(i[0])


async def action_simple_text(message):
    await dell_message(message.chat.id)
    await add_message_history(user_id=message.from_user.id,
                              message_id=message.message_id)


# Action when detected new user
async def action_new_user(message):
    msg = await message.answer(f"Привіт, {message.chat.first_name} 😊\n\n"
                               f"На зв'язку чат-бот F-3. \n\n"
                               f"Зі мною ви можете:\n"
                               f"-Придбати абонемент.\n"
                               f"-Записатись на масаж.\n"
                               f"-Назначити дату та час тренування.\n"
                               f"-Отримати відповіді на будь які питанні .\n\n"

                               f" Для реєстрації в боті надайте свій номер телефону.",
                               reply_markup=reply_get_contact)
    await add_message_from_bot(msg)
    await Reg.phone.set()


# Decorator for check user
def decorator_check_user(func):
    """
    Декоратор який перевіряє чи користувач зарегестрований
    якщо ні то перенаправляє на регестрацію

    :param func:
    :return:
    """
    async def wrepper(*args, **kwargs):
        message = args[0]

        await action_simple_text(message)

        if await check_user(message.from_user.id):
            try:
                await func(message, kwargs['state'])
            except TypeError:
                await func(message)
        else:
            await action_new_user(message)
    return wrepper


# Decorator for check admin
def decorator_check_admin(func):
    async def wrepper(*args, **kwargs):
        message = args[0]

        if await check_admin(message.from_user.id):
            await action_simple_text(message)
            try:
                await func(message, kwargs['state'])
            except TypeError:
                await func(message)
        else:
            await add_message_history(user_id=message.from_user.id,
                                      message_id=message.message_id)
    return wrepper


# Decorator for check trainer
def decorator_check_trainer(func):
    async def wrepper(*args, **kwargs):
        message = args[0]

        if await check_trainer(message.from_user.id):
            await action_simple_text(message)
            try:
                await func(message, kwargs['state'])
            except TypeError:
                await func(message)
        else:
            await add_message_history(user_id=message.from_user.id,
                                      message_id=message.message_id)
    return wrepper


# Status trainer
def status_trainer(status_id) -> str:
    if status_id == 1:
        status = 'active'
    else:
        status = 'no active'
    return status





async def callback_ending(callback) -> int:
    """
    Отримуємо закінчення данних callback.
    Все що йде після -

    :param callback:
    :return int:
    """

    return int(callback.data.split("-")[1])


def get_data_from_fetchall(values):
    if values:
        return values[0][0]
    else:
        return []


def get_data_from_fetchall0(values):
    if values:
        return values[0][0]
    else:
        return 0


async def get_chois_data(state) -> str:
    year = await get_current_year()
    training_data = await state.get_data()
    chois_data = f"{year}-{training_data['last_month']}-{training_data['choised_day']}"

    return chois_data


# Викликаэмо після успішної зміни данних для переходу в головне меню
async def well_done_client(message, state):

    msg = await message.answer(text='Зміни успішно виконанні✅')

    await add_message_from_bot(msg)
    await state.finish()

    await sleep_time(2)
    await ent_in_menu(message.chat.id)












