import os
import logging

from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import *

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

import asyncio
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

available_users = {"840649297", }

@dp.message(Command("start"))
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id in available_users:
        await message.answer(f"Yes")
    else:
        await message.answer(f"No")
    await message.answer(f"user id: {user_id}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())
