from aiogram.dispatcher.filters.state import StatesGroup, State


class Weather(StatesGroup):
    where = State()
    when = State()
