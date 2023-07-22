from datetime import datetime, timedelta

start_date = datetime(2023, 12, 30)


# result_date = start_date + timedelta(days=4)

new_format = start_date.strftime('%Y-%m-%d')

print(new_format)