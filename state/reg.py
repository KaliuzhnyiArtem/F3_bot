from aiogram.dispatcher.filters.state import State, StatesGroup


class Reg(StatesGroup):
    phone = State()


class Adm(StatesGroup):
    group_msg = State()


class Card(StatesGroup):
    getphoto = State()
    getname = State()
    change_trainer_status = State()
    getdescription = State()


class RegWorker(StatesGroup):
    choise_work = State()


class SerachClient(StatesGroup):
    get_client_name = State()


class ClientCard(StatesGroup):
    edit_name = State()
    edit_phone = State()
    edit_trainer = State()
    edit_commet = State()
