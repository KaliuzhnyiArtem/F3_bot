from datetime import datetime

from database.frezz_db import get_ls_freez_by_id_member


def delta_day(start_date, end_date):
    date1 = start_date
    date2 = end_date

    # Обчислюємо різницю між датами
    delta = date2 - date1

    # Отримуємо кількість днів
    days = delta.days
    return days


async def day_used(id_client_membership):
    """
    Повертаэ скікільки днів вж евикористано в заморозці

    :return:
    """
    sum_day = 0
    ls_freez = await get_ls_freez_by_id_member(id_client_membership)
    for freez in ls_freez:
        start_day = freez[0]
        if freez[1]:
            end_day = freez[1]
        else:
            end_day = datetime.today().date()

        delta = delta_day(start_day, end_day)
        if delta == 0:
            sum_day += 1
        elif delta > 0:
            sum_day += delta+1

    return sum_day



