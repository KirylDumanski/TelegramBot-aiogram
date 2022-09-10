from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN

# Project Init
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    """Print the message when the bot starts"""
    print('BOT ONLINE!')


@dp.message_handler()
async def echo(message: types.Message):
    """Echo bot"""
    await bot.send_message(message.from_user.id, message.text)


# Polling
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
