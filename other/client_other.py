from database.memberships_db import check_client_trial_training, check_client_membership, check_client_trial_history, \
    info_membersips2, check_client_membership2, check_client_trial_training2, set_start_date_membership, \
    check_client_membership_by_idabon
from database.search_client_db import find_client_by_id
from database.training_history_db import get_planed_training, get_planed_trial_training
from database.user_db import get_id_trainer_client
from other.membership_othre import acces_count_training, count_training_history, \
    count_trial_training_history
from aiogram import types

from other.trainer_other import trainer_name


async def get_client_id(telegram_id):
    """
    Повертає ід клєінта отримавши телеграм ід
    :param telegram_id:
    :return:
    """
    client_id = await find_client_by_id(telegram_id)
    if client_id:
        return client_id[0][0]
    else:
        return 0


async def get_trainer_id_client(telegram_id):
    trainer_id = await get_id_trainer_client(telegram_id)
    if trainer_id:
        if trainer_id[0][0] is not None:
            return trainer_id[0][0]
        else:
            return 0
    else:
        return 0


async def check_show_trial_trainig(telegram_id):
    """
    Робить перевірку чи було у клієнта пробне тренування або оплачений абонемент
    необхідно для відображення пробного тренування в меню
    :param telegram_id:
    :return:
    """

    client_id = await find_client_by_id(telegram_id)
    if client_id:
        client_id = client_id[0][0]
        if await check_client_membership2(client_id) or await check_client_trial_training(client_id):
            return False
        else:
            return True
    return False


async def acces_choise_data_trainig(telegram_id):
    """
    Метод дозволяє або забороняє доступ до бронювання дати треування.
    Дозвіл якщо у клієнта є оплачений абонемент або пробне тренування
    :param telegram_id:
    :return:
    """

    client_id = await find_client_by_id(telegram_id)
    if client_id:
        client_id = client_id[0][0]
        if await check_client_membership(client_id) \
                and await acces_count_training(telegram_id):
            return True
        elif await check_client_trial_training(client_id) and not await check_client_trial_history(client_id):
            return True
        return False


async def type_trening(telegram_id):
    """
    Визначає тип тренування пробне чи звичайне. Приорітет на пробному тренуванні

    :param telegram_id:
    :return:
    """
    client_id = await find_client_by_id(telegram_id)
    if client_id:
        client_id = client_id[0][0]
        if await check_client_trial_training(client_id) and not await check_client_trial_history(client_id):
            return 'trial'
        elif await check_client_membership(client_id):
            return 'training'
        else:
            return None


async def info_client(message: types.Message):
    """
    Повертає строку яка містітить інформацію про клієнта для відображення в особистому кабінеті
    :return:
    """
    info = f'🖐🏻Привіт {message.from_user.first_name}\n\n'
    tg_id_client = message.from_user.id

    name_trainer = await _trainer_name(tg_id_client)

    info_memberships = await _memberships_info(tg_id_client)
    info_planed_training = await _planed_trainig(tg_id_client)

    if name_trainer:
        info += f'🏋️Ваш тренер: {name_trainer}\n\n'
    else:
        info += f'🏋️Ваш тренер: не назначений\n\n'

    if info_memberships:
        info += f'💳Активні абонементи:\n' \
                f'{info_memberships}'
    else:
        info += 'У вас немає активного абонементу\n\n'

    if info_planed_training:
        info += f'📅Заплановані тренування \n' \
                f'{info_planed_training}'

    return info


async def client_info_for_admin(tg_id_clint, client_info, trainer_name):


    info = f'Картка клієнта:\n\n'
    name = f'Імя: {client_info[1]}\n'
    phone = f'Телефон: {client_info[3]}\n'
    tg_username = f'Tg username: {client_info[2]}\n\n'
    comment = f'Коментар: {client_info[5]}\n\n'
    trainer = f'Тренер: {trainer_name}\n\n'

    info += name+phone+tg_username+comment+trainer

    info_memberships = await _memberships_info(tg_id_clint)
    info_planed_training = await _planed_trainig(tg_id_clint)

    if info_memberships:
        info += f'💳Активні абонементи:\n' \
                f'{info_memberships}'
    else:
        info += 'У вас немає активного абонементу\n\n'

    if info_planed_training:
        info += f'📅Заплановані тренування \n' \
                f'{info_planed_training}'

    return info





async def _trainer_name(tg_id: int):
    """Повертає імя фамілію тренере клієнта по ід"""
    trainer_id = await get_trainer_id_client(tg_id)
    return await trainer_name(trainer_id)


async def _memberships_info(tg_id):
    '''
    Формує текст з інформацією про абонементи для особистого кабінета.
    :param tg_id:
    :return:
    '''

    client_id = await get_client_id(tg_id)
    ls_member = await check_client_membership(client_id)
    trial_training = await check_client_trial_training2(client_id)

    rez = []
    if trial_training:
        abon_name = 'Пробне тренування'

        done_training = await count_trial_training_history(client_id)
        amount_training = f'({done_training}/1)'
        by_abon_data = trial_training[0][2]
        activity_month = 1

        new_month = str(int((str(by_abon_data).split('-'))[1])+activity_month)

        new_data = (str(by_abon_data).split('-'))
        new_data[1] = new_month
        new_data = '-'.join(new_data)

        rez.append([abon_name, amount_training, new_data])

    for client_abon in ls_member:
        abot_info = await info_membersips2(client_abon[2])
        abon_name = abot_info[0][0]

        done_training = await count_training_history(client_abon[0])
        amount_training = f'({done_training}/{abot_info[0][2]})'

        new_data = ': Не активований'
        if client_abon[3]:
            by_abon_data = client_abon[3]
            activity_month = abot_info[0][1]
            new_month = str(int((str(by_abon_data).split('-'))[1])+activity_month)

            new_data = (str(by_abon_data).split('-'))
            new_data[1] = new_month
            new_data = '-'.join(new_data)

        rez.append([abon_name, amount_training, new_data])

    if rez:
        text = ''
        for abon in rez:
            text += f"- {abon[0]} {abon[1]}\n дійсний до {abon[2]}\n\n"
        return text


async def _planed_trainig(tg_id):
    client_id = await get_client_id(tg_id)
    training_list = await get_planed_training(client_id)
    trial_training = await get_planed_trial_training(client_id)
    text = ''
    if training_list:
        for training in training_list:
            text += f'- {training[3]} на {training[4]}\n'

    if trial_training:
        for training in trial_training:
            text += f'- {training[3]} на {training[4]}\n'
    return text


async def _check_client_trainer(tg_id_client: int):
    trainer_id = await get_trainer_id_client(tg_id_client)
    if trainer_id:
        return True
    else:
        return False


async def count_freez_day(id_client_membership):
    '''
    Повертає скількі дні абонемент клієнта був на паузі
    :return:
    '''
    pass


async def def_check_start_date(id_client_membership, date_activate):
    """
    Перевіряє, чи це не перше тренування в абонементі,
     якщо так то встановлю дату активаціїї абонемента
    :return:
    """
    client_membership = await check_client_membership_by_idabon(id_client_membership)
    if not client_membership[0][3]:
        await set_start_date_membership(id_client_membership, date_activate)
















