from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.keyboards import kb_main_menu
from loader import dp


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    user_full_name = message.from_user.full_name
    await message.reply(f'Привет, {user_full_name}! Рад видеть тебя! Сделай выбор.', reply_markup=kb_main_menu)
