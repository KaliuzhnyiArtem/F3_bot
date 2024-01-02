import time
from aiogram import types


# Sleap
from database.memberships_db import select_membership
from database.msg_id_history_db import add_message_from_bot
from keybords.menu_buttons import create_inline_membr


async def sleep_time(sec):
    time.sleep(sec)


async def show_all_memeberships(command, message: types.Message):
    for i in await select_membership():
        if i[1] == 'Програма F3':
            msg = await message.answer(f'💳Абонемент: {i[1]}\n\n'
                                       f'🏋🏻Перелік послуг:\n'
                                       f'- {i[4]} тренуваннь з тренером\n'
                                       f'- рекомендації по раціону харчування від дієтолога\n'
                                       f'- контроль харчування дієтологом\n'
                                       f'- заміри параметрів тіла раз на тиждень\n'
                                       f'- фото "до/після" раз на тиждень\n\n'
                                       f'⏳Термін дії - {i[3]} місяць\n\n'
                                       f'▪️Ціна: {i[2]} грн',
                                       reply_markup=await create_inline_membr(i[0], command),
                                       parse_mode='HTML',
                                       disable_notification=False)

            await add_message_from_bot(msg)

        else:
            msg = await message.answer(f'💳Абонемент: {i[1]}\n\n'
                                       f'🏋🏻Перелік послуг:\n'
                                       f'- {i[4]} тренуваннь з тренером\n\n'
                                       f'⏳Термін дії - {i[3]} місяць\n\n'
                                       f'▪️Ціна: {i[2]} грн',
                                       reply_markup=await create_inline_membr(i[0], command),
                                       parse_mode='HTML',
                                       disable_notification=False)

            await add_message_from_bot(msg)
