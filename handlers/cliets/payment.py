# Aiogram
from loader import dp, bot
from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext

# Database
from database.msg_id_history_db import add_message_history


# Підтвердження готовності товару до покупки
from other.payment_other import payment_trial_trainig, payment_membersip, payment_massage


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Action after payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):
    await add_message_history(user_id=message.from_user.id,
                              message_id=message.message_id)

    pay_information = list(message.successful_payment.to_python().values())
    paymented_item = pay_information[2]

    if paymented_item == 'trial_training':
        await payment_trial_trainig(message)

    elif paymented_item == 'membership':
        await payment_membersip(message, state)

    elif paymented_item == 'massage':
        await payment_massage(message)
