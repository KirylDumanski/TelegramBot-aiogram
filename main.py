import sqlite3
from datetime import datetime
from typing import Tuple

import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import config

# Project Init
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# SQL Init
connection = sqlite3.connect('db.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS rates(
    date TEXT PRIMARY KEY,
    usd TEXT,
    eur TEXT,
    rub TEXT
    )""")

# Global vars
TODAY_W0 = '{dt.year}-{dt.month}-{dt.day}'.format(dt=datetime.today())  # without leading zeroes, ex: 2022-3-9

# Keyboards
kb_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
btn_rates = KeyboardButton('Курсы валют 💰')
btn_weather = KeyboardButton('Погода 🌞')
kb_main_menu.add(btn_rates, btn_weather)

# Keyboards - Rates
kb_rates_when = ReplyKeyboardMarkup(resize_keyboard=True)
btn_rates_on_today = KeyboardButton('На сегодня 📅')
btn_rates_on_date = KeyboardButton('На дату 📅')
kb_rates_when.add(btn_rates_on_today, btn_rates_on_date)

# Keyboards - Weather
kb_weather_where = ReplyKeyboardMarkup(resize_keyboard=True)
btn_weather_brest = KeyboardButton('Брест')
btn_weather_vitebsk = KeyboardButton('Витебск')
btn_weather_gomel = KeyboardButton('Гомель')
btn_weather_grodno = KeyboardButton('Гродно')
btn_weather_minsk = KeyboardButton('Минск')
btn_weather_mogilev = KeyboardButton('Могилев')
kb_weather_where.add(btn_weather_brest, btn_weather_vitebsk, btn_weather_gomel, btn_weather_grodno,
                     btn_weather_minsk, btn_weather_mogilev)


# States
class RatesGetDate(StatesGroup):
    date_text = State()


class Weather(StatesGroup):
    where = State()
    when = State()
    on_date = State()


# Util
async def on_startup(_):
    """Print the message when the bot starts"""
    print('BOT ONLINE!')


# Message handlers - Commands
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_full_name = message.from_user.full_name
    await message.reply(f'Привет, {user_full_name}! Рад видеть тебя! Сделай выбор.', reply_markup=kb_main_menu)


@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply('Чем я могу тебе помочь?')


# Message handlers - User - Weather
@dp.message_handler(Text(equals=['Погода 🌞']))
async def weather(message: types.Message):
    await message.reply('Где вас интересует погода?', reply_markup=kb_weather_where)
    await Weather.where.set()


@dp.message_handler(state=Weather.where)
async def forecast(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(where=answer)
    city: dict = await state.get_data('where')
    text = get_weather(city['where'])
    await message.reply(text, reply_markup=kb_main_menu)
    await state.finish()


# Message handlers - User - Rates
@dp.message_handler()
async def exchange_rates(message: types.Message):
    if message.text == 'Курсы валют 💰':
        await message.reply('На когда?', reply_markup=kb_rates_when)

    if message.text == 'На сегодня 📅':
        await send_rates(message, TODAY_W0)
    if message.text == 'На дату 📅':
        await message.reply('Введите дату в формате ГГГГ-ММ-ДД\nНапример: 2022-09-01')
        await RatesGetDate.date_text.set()


@dp.message_handler(state=RatesGetDate.date_text)
async def get_date_from_user(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(date_text=answer)

    date_text: dict = await state.get_data('date_text')

    try:
        await send_rates(message, date_text['date_text'])
        await state.finish()

    except ValueError:
        await message.answer("Неверный формат даты. Должен быть ГГГГ-ММ-ДД")
        answer = message.text
        await state.update_data(date_text=answer)


# Misc - Rates
def get_rates_from_server(date_text: str) -> None:
    """Get exchange rates (usd, eur, rub) through the API of the National Bank
    of the Republic of Belarus and add them to the database  """

    req = requests.get(f'https://www.nbrb.by/api/exrates/rates?ondate={date_text}&periodicity=0')
    USD = EUR = RUB = None
    if req.status_code == 200:
        for i in req.json():
            if i['Cur_Abbreviation'] == 'USD':
                USD = i['Cur_OfficialRate']
            if i['Cur_Abbreviation'] == 'EUR':
                EUR = i['Cur_OfficialRate']
            if i['Cur_Abbreviation'] == 'RUB':
                RUB = i['Cur_OfficialRate']

    cursor.execute("""INSERT INTO rates VALUES(?,?,?,?)""", (date_text, USD, EUR, RUB))
    connection.commit()


def date_format_validate(date_text: str) -> str:
    """Check if user input date formatted YYYY-MM-DD without leading zeroes"""
    try:
        user_date = '{dt.year}-{dt.month}-{dt.day}'.format(dt=datetime.strptime(date_text, '%Y-%m-%d'))
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    return user_date


def get_actual_rates(date_text: str) -> tuple:
    """Get exchange rates from the database, if they are missing, calls the function
    get_rates_from_server and returns a tuple with exchange rates"""

    date = date_format_validate(date_text)
    cursor.execute("""SELECT usd, eur, rub FROM rates WHERE date=?""", (date,))

    result = cursor.fetchall()  # [('2.5517',)]

    if result:
        return result[0]
    else:
        get_rates_from_server(date)
        cursor.execute("""SELECT usd, eur, rub FROM rates WHERE date=?""", (date,))
        result = cursor.fetchall()
        return result[0]


async def send_rates(message: types.Message, date_text: str) -> None:
    """Sends exchange rates to chat"""
    rates: Tuple[str] = get_actual_rates(date_text)
    message_text = f"""Курсы валют НБРБ на {date_text}:
---------------------------------------------------
{rates[0].ljust(6, '0')} BYN - 1 Доллар 🇺🇸 
{rates[1].ljust(6, '0')} BYN - 1 Евро 🇪🇺 
{rates[2].ljust(6, '0')} BYN - 100 Рос.рублей 🇷🇺 """
    await message.reply(message_text, reply_markup=kb_main_menu)


# Misc - Weather
city_id = {'Минск': 625144,
           'Брест': 629634,
           'Витебск': 620127,
           'Гомель': 627907,
           'Гродно': 627904,
           'Могилев': 625665
           }


def get_weather(city: str) -> str:
    """Get request from OpenWeatherMap API and return parsed string"""
    params = {'id': city_id[city],
              'units': 'metric',
              'lang': 'ru',
              'appid': config.WEATHER_TOKEN}
    data = requests.get('https://api.openweathermap.org/data/2.5/weather?', params=params).json()
    # Parsing json
    time = datetime.fromtimestamp(data['dt']).time()
    temp = round(data['main']['temp'])
    feels_like = round(data['main']['feels_like'])
    pressure = round(data['main']['pressure'] / 1.333)
    city = data['name']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).time()
    sunset = datetime.fromtimestamp(data['sys']['sunset']).time()
    weather_desc = data['weather'][0]['description'].capitalize()
    wind_speed = data['wind']['speed']

    text = f"<u>В городе {city} по состоянию на {time}</u>:\n" \
           f"{weather_desc}.\n" \
           f"Температура {temp}°C, ощущается как {feels_like}°C\n" \
           f"Ветер: {wind_speed} м/с.\n" \
           f"Атмосферное давление: {pressure} мм. рт. ст.\n" \
           f"\n" \
           f"Восход: {sunrise}\n" \
           f"Закат: {sunset}"

    return text


# Polling
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
