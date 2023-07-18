# Aiogram
from loader import dp, bot
from aiogram import types
from aiogram.types import LabeledPrice, ContentType

# Database
from database.msg_id_history_db import add_message_from_bot

# Other
from keybords.menu_buttons import r_back_to_menu
from other.func_other import decorator_check_user
from config import PAYMENT_TOKEN


@dp.message_handler(lambda message: message.text == "🏋️Записатись на пробне тренування")
@decorator_check_user
async def trial_trainig(message: types.Message):
    msg = await message.answer('👋Ласкаво просимо в меню запису на пробне тренування\n\n'
                               '- На першому тренуванні ви ознайомитесь з залом\n'
                               '- Ми визначимо ваші цілі\n'
                               '- Обговоримо особливості вашого організму, '
                               'щоб створити індивідуальний тренувальний план,'
                               ' який буде максимально підходити вам.\n\n'
                               '▪️Ціна 250 грн.\n\n'
                               '🏃🏻Не зволікайте, записуйтесь на пробне тренування вже сьогодні '
                               'та почніть свій шлях до здорового та активного життя!',
                               reply_markup=r_back_to_menu
                               )
    await add_message_from_bot(msg)

    msg = await bot.send_invoice(
        chat_id=message.from_user.id,
        title=f'Пробне тренування',
        description='Ви за крок до спортивного та здорового тіла😎',
        payload='trial_training',
        provider_token=PAYMENT_TOKEN,
        currency='UAH',
        prices=[
            LabeledPrice(
                label=f'Пробне тренування',
                amount=250 * 100
            ),
        ],
    )
    await add_message_from_bot(msg)
