from database.msg_id_history_db import add_message_from_bot
from database.training_history_db import get_all_planed_training, chang_trial_training_status, chang_training_status
from keybords.trainer_menu import r_back_to_trainer_menu, be_or_not_be
from other.func_other import dell_message, get_chois_data
from other.trainer_other import get_traniner_id, info_about_training


async def training_list_for_treiner(callback, state):
    """
    Виводить список всіх запланованих тренувань тренера
    """
    msg = await callback.message.answer(f'Список тренувань', reply_markup=r_back_to_trainer_menu)
    await dell_message(callback.from_user.id)
    await add_message_from_bot(msg)

    trainer_id = await get_traniner_id(callback.from_user.id)

    if callback.data.startswith('trlist'):
        await state.update_data(choised_day=callback.data.split("-")[1])

    cois_date = await get_chois_data(state)

    ls_training = await get_all_planed_training(trainer_id, cois_date)

    if ls_training:
        for training in ls_training:
            msg = await callback.message.answer(await info_about_training(training),
                                                reply_markup=await be_or_not_be(training[0], training[3]))
            await add_message_from_bot(msg)

    else:
        msg = await callback.message.answer(f'На {cois_date}\n'
                                            f'Немає запланованих тренувань')
        await add_message_from_bot(msg)


async def cheng_training_status(type_training, status, id_training):
    if type_training == 'trial':
        await chang_trial_training_status(id_training, status)
    else:
        await chang_training_status(id_training, status)