from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.keyboards import kb_rates_when
from loader import dp
from misc.get_and_send_rates import send_rates
from states.rates import Rates

TODAY_W0 = '{dt.year}-{dt.month}-{dt.day}'.format(dt=datetime.today())  # without leading zeroes, ex: 2022-3-9


@dp.message_handler(Text(equals=['Курсы валют 💰']))
async def exchange_rates(message: types.Message):
    await message.reply('На когда?', reply_markup=kb_rates_when)
    await Rates.when.set()


@dp.message_handler(text=['На сегодня 📅'], state=Rates.when)
async def rates_on_today(message: types.Message, state: FSMContext):
    await send_rates(message, TODAY_W0)
    await state.finish()


@dp.message_handler(Text(equals=['На дату 📅']), state=Rates.when)
async def rates_on_date(message: types.Message):
    await message.reply('Введите дату в формате ГГГГ-ММ-ДД\nНапример: 2022-09-01')
    await Rates.date_text.set()


@dp.message_handler(state=Rates.date_text)
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
