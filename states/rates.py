from aiogram.dispatcher.filters.state import StatesGroup, State


class Rates(StatesGroup):
    when = State()
    on_today = State()
    on_date = State()
    date_text = State()