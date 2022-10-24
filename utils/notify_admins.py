import logging

from aiogram import Dispatcher

from data.config import ADMIN


async def on_startup_notify(dp: Dispatcher):
    try:
        text = 'Bot started!'
        await dp.bot.send_message(ADMIN, text)
    except Exception as err:
        logging.exception(err)
