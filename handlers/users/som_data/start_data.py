import datetime
import os
import random
import zipfile

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile
from telethon import TelegramClient

from keyboards.default import menu_start
from keyboards.default.start_menu import menu_start_data, menu_beck
from loader import dp, bot


@dp.message_handler(text='💻 Данные', state='*')
async def start(message: types.Message, state: FSMContext):

    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 💻 Данные</b>\n\n"
                         f"<b>⚪️Session</b> - Добавление вашего аккаунта с него будет происходить "
                         f"парсинг и рассылка по вашим каналам;\n\n"
                         f"<b>⚫️Proxy</b> - Еужно добавить, что бы не забанило все аккаунты;\n\n"
                         f"<b>🔵Accounts</b> - Если мы не добавим аккаунты, "
                         f"мы не сможем рассылать и инвайтить.\n\n"
                         f"<b>🟢Create</b> - Создать сессию", reply_markup=menu_start_data)

@dp.message_handler(text='🟢Create', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"⚡️Отправьте мне ваш номер телефона <code>79493158791</code> <b>(Плюсики, пробелы, скобочки 🔴НЕНАДА)\n"
                         f"Пример:</b>",
                         reply_markup=menu_beck)

    await message.answer(f"79493158791")
    await state.set_state('createsession')

@dp.message_handler(state='createsession')
async def add_channel_get_photo(message, state: FSMContext):
    nomber = message.text
    api_hash = f'114f5f726cd5540966760aa9267bf99b'

    client = TelegramClient(rf'data/new.session', 1871428, api_hash)
    await client.connect()
    await state.update_data(nomber=nomber)
    if not await client.is_user_authorized():
        await client.send_code_request(nomber)

        await state.set_state('createsession_2')
        await message.answer(f"⚡️Отправьте мне ваш код")




@dp.message_handler(state='createsession_2')
async def code_callback(message, state: FSMContext):
    api_hash = f'114f5f726cd5540966760aa9267bf99b'
    client = TelegramClient(rf'data/new.session', 1871428, api_hash)
    await client.connect()
    nom = await state.get_data()
    nomber = nom['nomber']
    if not await client.is_user_authorized():
        await client.sign_in(nomber, message.text)
    await state.finish()
    await client.disconnect()
    await bot.send_document(message.from_user.id, InputFile(rf"data/new.session", filename=f'start.session'))

    os.remove(rf"data/new.session")
    await message.answer(f"⚡️Сессия создана")





@dp.message_handler(text='⚪️Session', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"⚡️Отправьте мне файл вашей <code>.session</code>, одним файлом как <b>прикреплен пример ниже.</b>",
                         reply_markup=menu_beck)

    await bot.send_document(message.from_user.id, InputFile(rf"data/start.session", filename=f'start.session'))

    await state.set_state('newsession')

@dp.message_handler(text='⚫️Proxy', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"⚡️Отправьте мне файл вашей <code>proxy.txt</code>, одним файлом как <b>прикреплен пример ниже.</b>",
                         reply_markup=menu_beck)

    await bot.send_document(message.from_user.id, InputFile(rf"telegramusers/proxy.txt", filename=f'proxy.txt'))

    await state.set_state('newproxy')


@dp.message_handler(text='🔵Accounts', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"⚡️Отправьте мне файл <code>.zip</code>, одним файлом как <b>прикреплен пример ниже.</b>",
                         reply_markup=menu_beck)

    await bot.send_document(message.from_user.id, InputFile(rf"telegramusers/test.zip", filename=f'test.zip'))

    await state.set_state('newzip')





@dp.message_handler(state='newzip',content_types=['document'])
async def add_channel_get_photo(message, state: FSMContext):
    name_of_file = f'zip_{message.from_user.id}.zip'
    await message.document.download(name_of_file)
    session_path = f'telegramusers'
    file = zipfile.ZipFile(name_of_file)
    file.extractall(session_path)
    file.close()
    os.remove(name_of_file)
    sessions = os.listdir(session_path)

    await message.answer(f"🔥Отлично, мы получили .session в колличестве - <code>{len(sessions) - 2}</code>", reply_markup=menu_start_data)

    await state.finish()

@dp.message_handler(state='newproxy',content_types=['document'])
async def add_channel_get_photo(message, state: FSMContext):
    destination = rf"telegramusers/proxy.txt"
    await message.document.download(destination)

    await message.answer(f"🔥Отлично, мы получили файл <code>proxy.txt</code>", reply_markup=menu_start_data)

    await state.finish()

@dp.message_handler(state='newsession',content_types=['document'])
async def add_channel_get_photo(message, state: FSMContext):
    destination = rf"data/start.session"
    await message.document.download(destination)

    await message.answer(f"🔥Отлично, мы получили файл <code>.session</code>", reply_markup=menu_start_data)

    await state.finish()

