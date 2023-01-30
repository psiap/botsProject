from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨🏿‍💻Парсер"),
            KeyboardButton(text="🦹🏽‍♀️Клонер"),
            KeyboardButton(text="💻 Данные"),
        ],
        [
            KeyboardButton(text="🧛🏿‍♂️Рассылка"),
            KeyboardButton(text="🧙🏿Инвайт"),
        ],
        [
            KeyboardButton(text="🥷🏻Рассылка по чатам"),
        ],
    ],
    resize_keyboard=True
)

menu_start_data = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚪️Session"),
            KeyboardButton(text="🟢Create"),
        ],
        [
            KeyboardButton(text="⚫️Proxy"),
            KeyboardButton(text="🔵Accounts"),
        ],
        [
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)

menu_start_cloner = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🫡Указать данные"),

        ],
        [
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)


menu_beck = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)

menu_clon_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Клонируем"),
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)

menu_beck_inv = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Инвайтим"),
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)

menu_beck_spam = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Рассылаем"),
            KeyboardButton(text="🔙Назад"),
        ],
    ],
    resize_keyboard=True
)