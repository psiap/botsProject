import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from handlers.users.som_parser.a_parser import Parser_chat
from keyboards.default import menu_start
from keyboards.default.start_menu import menu_beck
from loader import dp, bot


@dp.message_handler(text='👨🏿‍💻Парсер', state='*')
async def start(message: types.Message, state: FSMContext):

    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 👨🏿‍💻Парсер</b>\n\n"
                         f"Отпавьте <b>штуку, по которой 🤴🏿 я смогу понять</b>, что это нужно парсить",reply_markup=menu_start)

    await state.set_state('parser')

@dp.message_handler(state='parser')
async def add_channel_get_photo(message, state: FSMContext):
    msg = await message.answer(f"🤴🏿 Я начал парсить")
    pc = Parser_chat(msg=msg)
    await pc.__start__(message.text)
    await state.finish()
    file = InputFile(
        fr"data/pars.csv"
    )
    await bot.send_document(chat_id=message.chat.id, document=file, caption=message.text,
                            reply_markup=menu_beck)
