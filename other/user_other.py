from keybords.admin_menu import generate_chois_worker
from loader import dp
from aiogram import types

# Database

from database.msg_id_history_db import add_message_from_bot


# Other

from other.trainer_other import get_trainers_info


async def show_trainer_list(message: types.Message):
    trainers_list = await get_trainers_info()

    if trainers_list:
        for trainer in trainers_list:
            trainer_comment = ''
            if trainer[4]:
                trainer_comment = trainer[4]
            caption = f'Тренер: {trainer[0]} {trainer[1]}\n\n' \
                      f'{trainer_comment}'

            msg = await message.answer_photo(photo=trainer[3],
                                             caption=caption,
                                             reply_markup=await generate_chois_worker(trainer[5], f"choisUser")
                                             )
            await add_message_from_bot(msg)
    else:
        msg = await message.answer('😕Нажаль зараз немає активних тренерів')
        await add_message_from_bot(msg)
