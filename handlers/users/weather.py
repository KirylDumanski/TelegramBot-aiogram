from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.keyboards import kb_main_menu, kb_weather_where
from loader import dp
from misc.get_weather import get_weather
from states.weather import Weather


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
