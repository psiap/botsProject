import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from handlers.helps.met_support import create_array_account_proxy, replaceter_text_in_aiogram
from handlers.users.som_inviter.a_invite import get_user_invaiter_tg_asyncio
from handlers.users.som_spam.a_spam import Spammer_in_tg_asyncio
from keyboards.default import menu_start
from keyboards.default.start_menu import menu_beck, menu_beck_inv, menu_beck_spam
from loader import dp, bot


@dp.message_handler(text='🧛🏿‍♂️Рассылка', state='*')
async def start(message: types.Message, state: FSMContext):
    proxy_file, sessions_len = create_array_account_proxy()
    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 🧙🏿Инвайт</b>\n\n"
                         f"<b>Аккаунтов для рассылки -</b> <code>{len(sessions_len)}</code>\n"
                         f"<b>Прокси для рассылки -</b> <code>{len(proxy_file)}</code>\n\n"
                         f"Что бы начать спамить пришлите базу\n"
                         f"Пример",reply_markup=menu_beck)

    file = InputFile(
        fr"data/spam_bd.csv"
    )
    await bot.send_document(chat_id=message.chat.id, document=file,
                            reply_markup=menu_beck)
    await state.set_state('spamdoc')

@dp.message_handler(state='spamdoc',content_types=['document'])
async def add_channel_get_photo(message, state: FSMContext):
    await message.document.download(rf'data\spam_bd.csv')
    await message.answer("Пришлите сообщение для рассылки\n"
                         "В данный момент поддерживается:\n"
                         "<b>Упитанный шрифт</b>\n"
                         "<i>Италик</i>\n"
                         "Гиперссылки\n"
                         "Фото")
    await state.set_state('spamtext')

@dp.message_handler(state='spamtext',content_types=['photo'])
async def add_channel_get_photo(message, state: FSMContext):
    new_text = await replaceter_text_in_aiogram(new_text=message.caption, array_caption=message.caption_entities)
    new_text = f"{new_text}~photo"
    with open(rf'data/text_spam.txt','w+',encoding='utf-8') as file:
        file.write(new_text)
    await state.finish()
    await message.answer("Начинаем рассылать?", reply_markup=menu_beck_spam)

@dp.message_handler(state='spamtext')
async def add_channel_get_photo(message: types.Message, state: FSMContext):
    new_text = await replaceter_text_in_aiogram(new_text=message.text, array_caption=message.entities)
    new_text = f"{new_text}~text"
    with open(rf'data/text_spam.txt','w+',encoding='utf-8') as file:
        file.write(new_text)
    await state.finish()
    await message.answer("Начинаем рассылать?", reply_markup=menu_beck_spam)


@dp.message_handler(text='🚀 Рассылаем', state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer('Рассылка началась', reply_markup=menu_beck)
    msg = await message.answer('Статус запущенно')
    pc = Spammer_in_tg_asyncio(msg=msg)
    await pc.__start__()
    await state.finish()
