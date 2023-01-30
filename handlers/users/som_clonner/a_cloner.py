import asyncio
import datetime
import os
import zipfile

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from handlers.helps.met_support import create_array_account_proxy
from handlers.users.som_clonner.mass_cloner_account import Update_photo_name_TG
from keyboards.default import menu_start
from keyboards.default.start_menu import menu_start_data, menu_beck, menu_start_cloner, menu_clon_start
from loader import dp, bot


@dp.message_handler(text='🦹🏽‍♀️Клонер', state='*')
async def start(message: types.Message, state: FSMContext):
    proxy_file, sessions_len = create_array_account_proxy()
    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 🦹🏽‍♀️Клонер</b>\n\n"
                         f"<b>Аккаунтов для клонирования -</b> <code>{len(sessions_len)}</code>\n"
                         f"<b>Прокси для клонирования -</b> <code>{len(proxy_file)}</code>\n\n"
                         f"Нажмите <b>🫡Указать данные</b> - что бы ввести данные",reply_markup=menu_start_cloner)

@dp.message_handler(text='🫡Указать данные', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Отправьте <b>Имя пользователя</b>\n"
                         f"Пример:")
    await message.answer(f"Иван", reply_markup=menu_beck)
    await state.set_state('clonename')


@dp.message_handler(state='clonename')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Отправьте <b>Фамилию пользователя</b>\n"
                         f"Пример:")
    await message.answer(f"Иванов", reply_markup=menu_beck)
    await state.update_data(name=message.text)
    await state.set_state('clonelastname')


@dp.message_handler(state='clonelastname')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Отправьте <b>БИО пользователя</b>\n"
                         f"Пример:")
    await message.answer(f"Менеджер по продажам газа в Европу", reply_markup=menu_beck)
    await state.update_data(lastname=message.text)
    await state.set_state('clonebio')

@dp.message_handler(state='clonebio')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Отправьте <b>Фото пользователя</b>\n"
                         f"Пример:")
    photo = InputFile(
        fr"data/avatar/1.png"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await state.update_data(bio=message.text)
    await state.set_state('clonephoto')

@dp.message_handler(state='clonephoto',content_types=['photo'])
async def add_channel_get_photo(message, state: FSMContext):
    await message.photo[-1].download(rf'data/avatar/1.png')
    data = await state.get_data()
    string_s = f"<b>У нас получилось:</b>\n" \
               f"Имя: {data['name']}\n" \
               f"Фамилия: {data['lastname']}\n" \
               f"БИО профиля: {data['bio']}\n\n" \
               f"<b>Клонируем аккаунты?</b>"

    photo = InputFile(
        fr"data/avatar/1.png"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=photo,caption=string_s,reply_markup=menu_clon_start)


@dp.message_handler(text='🚀 Клонируем', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"🚀 Клонируем началось")
    data = await state.get_data()
    up_photo = Update_photo_name_TG(static_first_name=data['name'],
                                    static_last_name=data['lastname'],
                                    static_img=fr"data/avatar/1.png",
                                    static_about=data['bio'])

    await up_photo.__start__()
    proxy_file, sessions_len = create_array_account_proxy()
    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 🦹🏽‍♀️Клонер</b>\n\n"
                         f"<b>Аккаунтов для клонирования -</b> <code>{len(sessions_len)}</code>\n"
                         f"<b>Прокси для клонирования -</b> <code>{len(proxy_file)}</code>\n\n"
                         f"Нажмите <b>🫡Указать данные</b> - что бы ввести данные\n\n"
                         f"<b>🚀 Клонирование закончилось закончилось</b>", reply_markup=menu_start_cloner)

