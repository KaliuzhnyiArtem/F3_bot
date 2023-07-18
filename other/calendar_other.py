

# Database
from database.training_history_db import get_training_by_date, count_trainings_on_times
from database.workers_dp import get_weekens_worker_by_mounth, get_day_with_training

# Other
from other.client_other import get_trainer_id_client, type_trening
from other.trainer_other import get_traniner_id, get_trainer_tg_id
import datetime
import calendar


async def get_current_mounth() -> int:
    return datetime.date.today().month


async def get_current_year() -> int:
    return datetime.date.today().year


async def get_current_day() -> int:
    return datetime.date.today().year


async def get_current_data() -> str:
    year = await get_current_year()
    month = await get_current_mounth()
    day = await get_current_day()
    return f'{year}-{month}-{day}'


async def generate_weeks(year, month) -> list:
    """
    Генерує дефолтний список тижнів заданого місяця

    :param year:
    :param month:
    :return: Повертає список тижнів, тижні представлені у вигляді списків з днями
    """
    weeks = []
    cal = calendar.monthcalendar(year, month)

    for week in cal:
        days = []
        for day in week:
            if day == 0:
                days.append(None)
            else:
                days.append(day)
        weeks.append(days)

    return weeks


async def generate_hours_table() -> list:
    colum1 = []
    colum2 = []
    colum3 = []

    for i in range(7, 12):
        if i == 7:
            colum1.append(f"{i}:30")
        else:
            colum1.append(f'{i}:00')
            colum1.append(f"{i}:30")

    for i in range(12, 17):
        if i == 16:
            colum2.append(f'{i}:00')
        else:
            colum2.append(f'{i}:00')
            colum2.append(f"{i}:30")

    for i in range(16, 21):
        if i == 16:
            colum3.append(f"{i}:30")
        else:
            colum3.append(f'{i}:00')
            colum3.append(f"{i}:30")

    return [colum1, colum2, colum3]


def get_name_month(nomb_month: int) -> str:
    name_month = ['Січень',
                  'Лютий',
                  'Березень',
                  'Квітень',
                  'Травень',
                  'Червень',
                  'Липень',
                  'Серпень',
                  'Вересень',
                  'Жовтень',
                  'Листопад',
                  'Грудень',
                  ]
    return name_month[nomb_month-1]


async def edit_generate_weeks(worker_tg_id: int, year: int, month: int, calendar_list: list) -> list:
    """
    Редагування отриманого календаря.
    Ставить смайлики на ті дні, на які вже назначені вихідні

    :param worker_tg_id:
    :param year:
    :param month:
    :param calendar_list:
    :return:
    """
    ls_weekends = await get_weekens_worker_by_mounth(worker_tg_id, month)

    for free_day in ls_weekends:
        for weeks in range(len(calendar_list)):
            if free_day[0].day in calendar_list[weeks]:
                value_index = calendar_list[weeks].index(free_day[0].day)
                calendar_list[weeks][value_index] = '🥳'
    return calendar_list


async def edit_day_with_trainings(worker_tg_id: int, year: int, month: int, calendar_list: list):
    """
    Редагує калентадь, перевіряє в які дні у тренера вже є тренування,
    і заміняє ці дні на смайкл з качком
    :return:
    """
    worker_id = await get_traniner_id(worker_tg_id)
    ls_day_with_training = await get_day_with_training(worker_id, month, year)

    for day_with_training in ls_day_with_training:
        for weeks in range(len(calendar_list)):
            if day_with_training[0].day in calendar_list[weeks]:
                value_index = calendar_list[weeks].index(day_with_training[0].day)
                calendar_list[weeks][value_index] = '🏋️'
    return calendar_list


async def filter_calendar_for_weekeds(worker_tg_id, year, month) -> list:
    """
    Фільтрує (редагує ) стандарний календарь для вихідних днів.
    Календарь виводиться адміну

    :param worker_tg_id:
    :param year:
    :param month:
    :return:
    """
    calendar_list = await generate_weeks(year, month)

    calendar_list = await edit_generate_weeks(worker_tg_id, year, month, calendar_list)
    calendar_list = await edit_day_with_trainings(worker_tg_id, year, month, calendar_list)
    return calendar_list


async def _edit_day_trainer_weekend(client_tg_id: int, year: int, month: int, calendar_list: list):
    """
    Перевірка для календаря бронювання тренування

    :param client_tg_id:
    :param year:
    :param month:
    :param calendar_list:
    :return:
    """
    defolt_trainer_id = await get_trainer_id_client(client_tg_id)
    trainer_tg_id = await get_trainer_tg_id(defolt_trainer_id)

    ls_weekends = await get_weekens_worker_by_mounth(trainer_tg_id, month)

    for free_day in ls_weekends:
        for weeks in range(len(calendar_list)):
            if free_day[0].day in calendar_list[weeks]:
                value_index = calendar_list[weeks].index(free_day[0].day)
                calendar_list[weeks][value_index] = None
    return calendar_list


async def _days_done(calendar_list: list, month: int):
    '''
    Прибирає з календаря дні які вже пройшли

    :param calendar_list:
    :param month:
    :return:
    '''
    day = datetime.date.today().day
    current_mounth = datetime.date.today().month

    if current_mounth == month:
        ls_day_done = [i for i in range(1, day)]
        for day_done in ls_day_done:
            for weeks in range(len(calendar_list)):
                if day_done in calendar_list[weeks]:
                    value_index = calendar_list[weeks].index(day_done)
                    calendar_list[weeks][value_index] = None
    return calendar_list


async def filter_calendar_for_training(client_tg_id: int, year: int, month: int) -> list:
    """
    Фільтрує (редагує ) стандарний календарь для назначення тренувань.


    :param client_tg_id:
    :param year:
    :param month:
    :return:
    """

    calendar_list = await generate_weeks(year, month)

    calendar_list = await _days_done(calendar_list, month)
    calendar_list = await _edit_day_trainer_weekend(client_tg_id, year, month, calendar_list)

    return calendar_list


async def only_one_training(client_tg_id: int, chois_data, hours_table):
    """
    Фільтр для відображення годин при бронюванні пробнобного тренування
    Скриває години якщо у тренера в цей час є хочаб 1 тренування

    :param client_tg_id:
    :param chois_data:
    :param hours_table:
    :return:
    """
    defolt_trainer_id = await get_trainer_id_client(client_tg_id)

    ls_training = await get_training_by_date(defolt_trainer_id, chois_data)

    for training in ls_training:
        for column in range(len(hours_table)):

            if training[0] in hours_table[column]:
                value_index = hours_table[column].index(training[0])
                hours_table[column][value_index] = None

    return hours_table


async def only_three_training(client_tg_id, chois_data, hours_table):
    '''
    Фільтр для відображення годин при бронюванні тренування
    Скриває години якщо у тренера в цей час є 3 або більше тренуваннь
    :return:
    '''
    defolt_trainer_id = await get_trainer_id_client(client_tg_id)

    ls_count_training = await count_trainings_on_times(defolt_trainer_id, chois_data)
    for trainings in ls_count_training:
        if trainings[1] >= 3:
            for column in range(len(hours_table)):
                if trainings[0] in hours_table[column]:
                    value_index = hours_table[column].index(trainings[0])
                    hours_table[column][value_index] = None

    return hours_table


async def filter_hour_inline(client_tg_id: int, chois_data):
    """
    Фільтрує (редагує ) стандарний меню вибору часу.
    :return:
    """

    tp_trainnig = await type_trening(client_tg_id)

    hours_table = await generate_hours_table()

    if tp_trainnig == 'trial':
        hours_table = await only_one_training(client_tg_id, chois_data, hours_table)

    hours_table = await only_three_training(client_tg_id, chois_data, hours_table)
    return hours_table


async def filter_calendar_for_trainer(year, month):
    '''
    Фільтрує календарь для відображення тренерам списка запланованих тренвань:
    :return:
    '''

    calendar_list = await generate_weeks(year, month)
    calendar_list = await _days_done(calendar_list, month)

    return calendar_list







