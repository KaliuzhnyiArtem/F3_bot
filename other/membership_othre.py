from database.client_membership_db import get_membershiop_id, edit_membership_status, edit_client_trial_status
from database.memberships_db import get_count_training, check_client_membership

from database.training_history_db import amount_training, get_planed_trial_training
from database.user_db import get_client_id





def get_from_fetchall(value):
    if value:
        return value[0][0]
    else:
        return None


async def count_training(member_id):
    value = await get_count_training(member_id)

    if value:
        return value[0][0]
    else:
        return 0


async def membership_id(user_member_id):
    value = await get_membershiop_id(user_member_id)
    if value:
        return value[0][0]
    else:
        return None

async def count_training_history(user_member_id):
    """
    Повертає кількість тренувань, з історїї тренувань. по заданому абонементу клієнта
    :param user_member_id:
    :return:
    """
    value = await amount_training(user_member_id)
    if value:
        return value[0][0]
    else:
        return None


async def count_trial_training_history(client_id):
    """
    Повертає кількість тренувань, з історїї тренувань. по заданому абонементу клієнта
    :param user_member_id:
    :return:
    """
    value = await get_planed_trial_training(client_id)
    if value:
        return 1
    else:
        return 0


async def get_user_member_id_by_tg_id(tg_id: int):
    client_id = get_from_fetchall(await get_client_id(tg_id))
    membership_id = get_from_fetchall(await check_client_membership(client_id))
    return membership_id


async def acces_count_training(tg_id):
    user_member_id = await get_user_member_id_by_tg_id(tg_id)
    member_id = await membership_id(user_member_id)
    count_train = await count_training(member_id)
    count_train_history = await count_training_history(user_member_id)

    if count_train <= count_train_history:
        return False
    else:
        return True


async def check_amount_training(tg_id):
    """
    Перевіряє скільки тренувань вже було у клієнта,
    якщо догнуло ліміту, змінює статус абонементу завершений
    :param tg_id:
    :return:
    """
    if not await acces_count_training(tg_id):
        user_member_id = await get_user_member_id_by_tg_id(tg_id)
        await edit_membership_status(user_member_id, 3)


async def check_amount_trial_training(client_id: int):
    """
        Перевіряє скільки тренувань вже було у клієнта,
    якщо догнуло ліміту, змінює статус абонементу завершений
    :param client_id:
    :return:
    """
    if await get_planed_trial_training(client_id):
        await edit_client_trial_status(client_id, 3)


async def check_start_date_membership():
    membership = await check_client_membership()
    return membership









