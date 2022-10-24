import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN,
          parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot=bot,
                storage=storage)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
