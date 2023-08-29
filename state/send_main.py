from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMessage(StatesGroup):
    wait_message_text = State()
    text_ready = State()