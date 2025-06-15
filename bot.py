import os
import logging

from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import *

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

pool = None

class Form(StatesGroup):
    top_up_stars_balance = State()


@dp.message(Command("start"))
async def handle_message(message: types.Message):
    await add_user(pool, message.from_user.id)
    stars = await get_stars(pool, message.from_user.id)
    await message.answer(f"You have been registered! You have {stars} stars.")

@dp.message(Command("create_invoice"))
async def create_invoice(message: types.Message, state : FSMContext):
    await message.answer("Write in the chat sum that you want to topup your stars balance")
    await state.set_state(Form.top_up_stars_balance)


@dp.message(Form.top_up_stars_balance)
async def topup_balance(message: types.Message, state : FSMContext):
    desired_sum = str(message.text)
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Stars in bot",
        description=f"You will top-up your balance with {int(desired_sum)} stars",
        payload="Top-up balance",
        currency="XTR",
        prices=[
            LabeledPrice(label="Stars", amount=int(desired_sum))
        ],
        start_parameter="test",
    )
    await state.clear()

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    user_id = str(message.from_user.id)
    payment = message.successful_payment

    await add_stars(pool, int(user_id), payment.total_amount)

    await message.answer(f"✅ Payment was successful!\n"
                         f"Sum: {payment.total_amount} Stars\n"
                         f"Desc: {payment.invoice_payload}")

async def main():
    global pool
    pool = await connect_db()
    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())
