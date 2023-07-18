from aiogram.dispatcher.filters.state import State, StatesGroup


class BookTrainig(StatesGroup):
    choise_date = State()
    choise_hour = State()