import logging

from decouple import config

import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config('SECRET_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer("Привет")
    await message.answer_sticker(r"CAACAgIAAxkBAAEIt5xkR4HL9QTpWYk6iQ6AgbxEPnDLqQACDioAAt1nQUpP0mg9dWgrSi8E")

if __name__ == '__main__':
    executor.start_polling(dp)