from aiogram.dispatcher.filters.state import State, StatesGroup

class Car(StatesGroup):
    surname = State()
    report = State()
    number = State()
    date = State()
    period = State()
    first_distance = State()
    last_distance = State()
    z_report = State()
    terminal = State()
    viza_discount = State()
    only_cash = State()
    cash_card = State()
    znf = State()
    perscash = State()
    bonuse = State()
    yandex_nal = State()
    yandex_bez = State()
    washing = State()
    type_pay_washing = State()
    azs = State()
    type_pay_azs = State()
    water = State()
    count_yandex = State()
    count_bavaria = State()
    over_cash = State()
    result = State()
    set_value = State()


class Admin(StatesGroup):
    admin = State()
    create_table = State()