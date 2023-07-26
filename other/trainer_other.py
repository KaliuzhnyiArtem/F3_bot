from database.adm_client_db import get_trainer_name
from database.search_client_db import get_info_client
from database.workers_dp import get_trainer_full_name, get_trainer_list_active, get_trainer_id_by_tg_id, \
    get_trainer_tg_id_by_id


async def trainer_name(trainer_id):
    name = await get_trainer_full_name(trainer_id)
    if name:
        return f"{name[0][0]} {name[0][1]}"
    else:
        return None


async def get_trainers_info():
    """
    Повртає список списків інформації про тренерів
    :return:
    """
    trainers_list = []
    for trainer in await get_trainer_list_active():
        trainers_list.append([trainer[0], trainer[1], trainer[2], trainer[3], trainer[4], trainer[5]])
    return trainers_list


async def get_traniner_id(trainer_id):
    trainer_id = await get_trainer_id_by_tg_id(trainer_id)
    if trainer_id:
        return trainer_id[0][0]
    else:
        return 0


async def get_trainer_tg_id(trainer_id):
    trainer_tg_id = await get_trainer_tg_id_by_id(trainer_id)
    if trainer_tg_id:
        return trainer_tg_id[0][0]
    else:
        return 0


async def get_name_trainer(id_trainer: int):
    if id_trainer:
        name, second_name = (await get_trainer_name(id_trainer))[0]
        return f'{name} {second_name}'
    else:
        return 'не назначений'


async def info_about_training(training_info) -> str:
    """
    Генерує текст з інформацією про тренування.
    Відображається коли тренер переглядає список запланованих тренувань
    """
    text = ''
    if training_info:
        client_info = await get_info_client(training_info[1])
        name_client = client_info[0][1]
        phone_client = client_info[0][3]
        time_training = training_info[2]

        if training_info[3] == 'trial':
            text = '‼️Пробне тренування‼️\n\n'

        text += f'Клієнт: {name_client}\n' \
                f'Телефон: {phone_client}\n'\
                f'Час тренування: {time_training}'
        return text
