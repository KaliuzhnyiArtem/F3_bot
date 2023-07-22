from datetime import datetime, timedelta


async def get_last_day_membersip(start_date, activity_month, freez_day):
    """
    Повертає дату до якого числа дійсний абонемент

    Типи абонемента:
    1 - пробне тренування
    2 - звичайне тренування
    """
    amount_days = freez_day+(activity_month*30)

    new_date = start_date + timedelta(days=amount_days)

    return new_date.strftime('%Y-%m-%d')
