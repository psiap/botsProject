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


@dp.message_handler(text='🥷🏻Рассылка по чатам', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Функция будет доступна 05.12.2022")
