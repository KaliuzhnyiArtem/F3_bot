from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API

storage = MemoryStorage()
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=storage)



