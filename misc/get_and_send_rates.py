from datetime import datetime

import requests
from aiogram import types

from keyboards.keyboards import kb_main_menu
from models.db_currency import connectDb

cursor, connection = connectDb()


def get_rates_from_server(date_text: str) -> None:
    """Get exchange rates (usd, eur, rub) through the API of the National Bank
    of the Republic of Belarus and add them to the database  """

    req = requests.get('https://www.nbrb.by/api/exrates/rates?',
                       params={'ondate': date_text, 'periodicity': 0})

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
    rates = get_actual_rates(date_text)
    message_text = f"""Курсы валют НБРБ на {date_text}:
---------------------------------------------------
{rates[0].ljust(6,'0')} BYN - 1 Доллар 🇺🇸 
{rates[1].ljust(6,'0')} BYN - 1 Евро 🇪🇺 
{rates[2].ljust(6,'0')} BYN - 100 Рос.рублей 🇷🇺"""
    await message.reply(message_text, reply_markup=kb_main_menu)
