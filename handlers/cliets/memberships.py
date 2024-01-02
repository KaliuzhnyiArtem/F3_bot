# Aiogram
from loader import dp, bot
from aiogram import types
from aiogram.types import LabeledPrice, ContentType
from aiogram.dispatcher import FSMContext

# Database
from database.memberships_db import info_membersips
from database.msg_id_history_db import add_message_from_bot

# Other
from keybords.menu_buttons import r_back_to_menu
from other.func_other import dell_message
from config import PAYMENT_TOKEN


@dp.callback_query_handler(lambda c: c.data.startswith('abon'))
async def action_member_inline(c: types.CallbackQuery, state: FSMContext):

    id_membersip = int(c.data.split('-')[1])
    memberships_info = await info_membersips(id_membersip)

    await c.answer('Чудовий вибір👍🏻')

    if memberships_info[1] == 'Програма F3':
        msg = await bot.send_message(c.from_user.id,
                                     f'💳Абонемент: {memberships_info[1]}\n\n'
                                     f'🏋🏻Перелік послуг:\n'
                                     f'- {memberships_info[4]} тренуваннь з тренером\n'
                                     f'- рекомендації по раціону харчування від дієтолога\n'
                                     f'- контроль харчування дієтологом\n'
                                     f'- заміри параметрів тіла раз на тиждень\n'
                                     f'- фото "до/після" раз на тиждень\n\n'
                                     f'⏳Термін дії - {memberships_info[3]} місяць\n\n'
                                     f'▪️Ціна: {memberships_info[2]} грн',
                                     reply_markup=r_back_to_menu,
                                     parse_mode='HTML'
                                     )
        await dell_message(c.from_user.id)
        await add_message_from_bot(msg)
    else:
        msg = await bot.send_message(c.from_user.id,
                                     f'💳Абонемент: {memberships_info[1]}\n\n'
                                     f'🏋🏻Перелік послуг:\n'
                                     f'- {memberships_info[4]} тренуваннь з тренером\n\n'
                                     f'⏳Термін дії - {memberships_info[3]} місяць\n\n'
                                     f'▪️Ціна: {memberships_info[2]} грн',
                                     reply_markup=r_back_to_menu,
                                     parse_mode='HTML'
                                     )
        await dell_message(c.from_user.id)
        await add_message_from_bot(msg)

    msg = await bot.send_invoice(
        chat_id=c.from_user.id,
        title=f'Абонемент: {memberships_info[1]}',
        description='Ви за крок до спортивного та здорового тіла😎',
        payload='membership',
        provider_token=PAYMENT_TOKEN,
        currency='UAH',
        prices=[
            LabeledPrice(
                label=f'Абонемент: {memberships_info[1]}',
                amount=memberships_info[2] * 100
            ),
        ],
    )
    await add_message_from_bot(msg)


    await state.update_data(id_membersip=id_membersip)


