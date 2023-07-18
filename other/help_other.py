#Aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

# Other
from keybords.calendar_inline import generage_calendar, inline_hour
from other.calendar_other import get_current_mounth, filter_calendar_for_weekeds, get_current_year, \
    filter_calendar_for_training, filter_hour_inline, filter_calendar_for_trainer


async def go_left_or_right(callback, state, command, worker_tg_id, place: str):
    """
    Обробрая натискання кнопок << >> в інлайн календарі
    Радегує попередньо виведений календарь відповідно до активованої кнопки

    :param callback:
    :param state:
    :param command:
    :param worker_tg_id:
    :return:
    """
    last_month = await state.get_data()
    current_month = await get_current_mounth()

    if callback.data == f'go-{command}_left' or callback.data == f'go-{command}_left':
        if last_month['last_month'] == 1 or last_month['last_month'] == current_month:
            await state.update_data(last_month=12)
        else:
            await state.update_data(last_month=last_month['last_month'] - 1)

        last_month = await state.get_data()
        current_calendar = None

        if place == 'training':
            current_calendar = await training_calendar(numb_month=last_month['last_month'],
                                                       command=f'{command}',
                                                       tg_id=worker_tg_id)
        elif place == 'weekend':
            current_calendar = await weeked_calendar(numb_month=last_month['last_month'],
                                                       command=f'{command}',
                                                       tg_id=worker_tg_id)
        elif place == 'trainer':
            current_calendar = await calendar_for_trainer(numb_month=last_month['last_month'],
                                                          command=f'{command}')

        await callback.message.edit_reply_markup(reply_markup=current_calendar)

    elif callback.data == f'go-{command}_right':
        if last_month['last_month'] == 12:
            await state.update_data(last_month=current_month)
        else:
            await state.update_data(last_month=last_month['last_month'] + 1)

        last_month = await state.get_data()

        current_calendar = None

        if place == 'training':
            current_calendar = await training_calendar(numb_month=last_month['last_month'],
                                                       command=f'{command}',
                                                       tg_id=worker_tg_id)
        elif place == 'weekend':
            current_calendar = await weeked_calendar(numb_month=last_month['last_month'],
                                                       command=f'{command}',
                                                       tg_id=worker_tg_id)
        elif place == 'trainer':

            current_calendar = await calendar_for_trainer(numb_month=last_month['last_month'],
                                                          command=f'{command}')

        await callback.message.edit_reply_markup(reply_markup=current_calendar)


async def weeked_calendar(numb_month: int, command: str, tg_id: int):
    """
    Генерує готовий інлайн календарь з вихідними днями та всіма фільтрами

    :param numb_month:
    :param command:
    :param tg_id:
    :return:
    """
    year = await get_current_year()

    calendar_list = await filter_calendar_for_weekeds(tg_id, year, numb_month)

    inline_calendar = await generage_calendar(numb_month=numb_month,
                                              command=command,
                                              mounth_list=calendar_list)
    return inline_calendar


async def training_calendar(numb_month: int, command: str, tg_id: int):
    """
    Генерує готовий інлайн календарь для бронювання тренувань, та всіма фільтрами

    :param type_training:
    :param numb_month:
    :param command:
    :param tg_id:
    :return:

    """

    year = await get_current_year()

    calendar_list = await filter_calendar_for_training(tg_id, year, numb_month)

    inline_calendar = await generage_calendar(numb_month=numb_month,
                                              command=command,
                                              mounth_list=calendar_list)
    return inline_calendar


async def hours_inline(tg_id: int, chois_data: str, place: str):
    """
    Генерує готовий інлайн меню для вибору часу тренувань, та всіма фільтрами
    :return:
    """

    hours_table = await filter_hour_inline(tg_id, chois_data)

    inline_calendar = await inline_hour(hours_table, place)
    return inline_calendar


async def calendar_for_trainer(numb_month: int, command: str):
    '''
    Генерує готовийі інлайн календарь для тренерів,
    для перегляду запланованих тренувань
    :return:
    '''
    year = await get_current_year()

    calendar_list = await filter_calendar_for_trainer(year, numb_month)
    inline_calendar = await generage_calendar(numb_month=numb_month,
                                              command=command,
                                              mounth_list=calendar_list)
    return inline_calendar





