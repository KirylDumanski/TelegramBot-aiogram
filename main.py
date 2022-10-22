import sqlite3
from datetime import datetime
from typing import Tuple

import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
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
kb_choice = ReplyKeyboardMarkup(resize_keyboard=True)
btn_rates = KeyboardButton('Курсы валют 💰')
kb_choice.add(btn_rates)

kb_rates_choose_date = ReplyKeyboardMarkup(resize_keyboard=True)
btn_on_today = KeyboardButton('На сегодня 📅')
btn_on_date = KeyboardButton('На дату 📅')
kb_rates_choose_date.add(btn_on_today, btn_on_date)


# States
class GetDate(StatesGroup):
    date_text = State()


# Util
async def on_startup(_):
    """Print the message when the bot starts"""
    print('BOT ONLINE!')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_full_name = message.from_user.full_name
    await message.reply(f'Привет, {user_full_name}! Рад видеть тебя! Сделай выбор.', reply_markup=kb_choice)


@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply('Чем я могу тебе помочь?')


@dp.message_handler()
async def exchange_rates(message: types.Message):
    if message.text == 'Курсы валют 💰':
        await message.reply('На когда?', reply_markup=kb_rates_choose_date)

    if message.text == 'На сегодня 📅':
        await send_rates(message, TODAY_W0)
    if message.text == 'На дату 📅':
        await message.reply('Введите дату в формате ГГГГ-ММ-ДД\nНапример: 2022-09-01')
        await GetDate.date_text.set()


@dp.message_handler(state=GetDate.date_text)
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
    await message.reply(message_text, reply_markup=kb_choice)


# Polling
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
