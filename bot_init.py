import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_ACCESS_TOKEN

storage = MemoryStorage()

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_ACCESS_TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot, loop=loop, storage=storage)
