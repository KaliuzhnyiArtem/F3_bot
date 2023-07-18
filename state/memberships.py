from aiogram.dispatcher.filters.state import State, StatesGroup


class MembershipsState(StatesGroup):
    choice_memberships = State()