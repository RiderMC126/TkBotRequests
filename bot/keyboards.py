from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def keyboard_start():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Отправить заявку")]
    ], 
    resize_keyboard=True, 
    one_time_keyboard=True)