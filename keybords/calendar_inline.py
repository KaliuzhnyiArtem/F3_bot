# Aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Other
from other.calendar_other import generate_hours_table

# Генеруємо список з назвами днів тижня
array_days = ['П', 'В', 'С', 'Ч', 'П', 'С', 'Н']
days_list = [InlineKeyboardButton(f'{i}', callback_data='nd') for i in array_days]

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


# Меню перелистування календаря для клієнта
async def generate_munu_calendar(numb_month, command):
    b_left = InlineKeyboardButton('<<', callback_data=f'go-{command}_left')
    b_right = InlineKeyboardButton('>>', callback_data=f'go-{command}_right')
    b_mounth = InlineKeyboardButton(f'{name_month[numb_month-1]}', callback_data='None')

    return [b_left, b_mounth, b_right]


# Меню перелистування календаря для клієнта
async def generate_munu_calendar_admin(numb_month, command):
    b_left = InlineKeyboardButton('<<', callback_data=f'go-{command}_left')
    b_right = InlineKeyboardButton('>>', callback_data=f'go-{command}_right')
    b_mounth = InlineKeyboardButton(f'{name_month[numb_month-1]}', callback_data='None')

    return [b_left, b_mounth, b_right]


async def generage_calendar(numb_month, command, mounth_list: list) -> InlineKeyboardMarkup:
    """
    Генерує інлайн клавіатуру календаря,
    відповідно переданому місяцю

    :param numb_month:
    :param command:
    :param mounth_list
    (Список тижнів, тижні представлені у вигляді стписків з днями):

    :return InlineKeyboardMarkup:
    """

    inline_calendar = InlineKeyboardMarkup(row_width=7)
    inline_calendar.add(*days_list)

    for week_id in mounth_list:
        week_list = []
        for day in week_id:
            if day is None:
                week_list.append(InlineKeyboardButton(' ', callback_data=f'None'))
            elif type(day) is int:
                week_list.append(InlineKeyboardButton(f'{day}', callback_data=f'{command}-{day}'))
            else:
                week_list.append(InlineKeyboardButton(f'{day}', callback_data=f'None'))
        inline_calendar.add(*week_list)

    inline_calendar.add(*await generate_munu_calendar(numb_month, command))

    return inline_calendar


# Генеруємо клавіатуру вибору часу тренування
async def inline_hour(hours_table, place: str):
    hours_inl = InlineKeyboardMarkup(row_width=3, )
    name_column1 = InlineKeyboardButton('Ранок️', callback_data='None')
    name_column2 = InlineKeyboardButton('Обід', callback_data='None')
    name_column3 = InlineKeyboardButton('Вечір', callback_data='None')
    hours_inl.add(name_column1, name_column2, name_column3)

    for column in range(len(hours_table)):
        for i in range(len(hours_table[column])):
            if hours_table[column][i] == 0:
                hours_table[column][i] = InlineKeyboardButton(f'0', callback_data=f'hour{place}-{hours_table[column][i]}')
            elif hours_table[column][i] is None:
                hours_table[column][i] = InlineKeyboardButton(' ', callback_data='None')
            else:
                hours_table[column][i] = InlineKeyboardButton(f'{hours_table[column][i]}',
                                                              callback_data=f'hour{place}-{hours_table[column][i]}')

    for i in range(9):
        hours_inl.add(hours_table[0][i], hours_table[1][i], hours_table[2][i])

    return hours_inl





