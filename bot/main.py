from aiogram.client.default import DefaultBotProperties
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter, Filter
from aiogram.types.input_file import FSInputFile
from aiogram.types import Message, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, BufferedInputFile, ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, types, F, Router, html
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import asyncio
import logging
import sys
from bot.config import *
from bot.keyboards import *
from bot.db import *


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
storage = MemoryStorage()
dp.fsm_storage = storage
router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Form(StatesGroup):
    ticket = State()


@dp.message(Command("start"))
async def start(message: Message):
    add_user(message)  # добавляем пользователя в базу
    await bot.send_message(
        message.chat.id,
        text="Здравствуйте! Я приму от вас заявку и отправлю её Администратору.",
        reply_markup=keyboard_start()
    )

@dp.message(F.text == "Отправить заявку")
async def sent_request(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, text="Введите текст для заявки:")
    await state.set_state(Form.ticket)

@dp.message(Form.ticket)
async def handle_ticket(message: Message, state: FSMContext):
    await state.update_data(ticket=message.text)
    data = await state.get_data()
    add_request(message, data['ticket'])
    await bot.send_message(message.chat.id, text="Ваша заявка принята! Администратор скоро с вами свяжется.")
    await state.clear()
    


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    asyncio.run(main())