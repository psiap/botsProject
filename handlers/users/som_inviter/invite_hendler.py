import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from handlers.helps.met_support import create_array_account_proxy
from handlers.users.som_inviter.a_invite import get_user_invaiter_tg_asyncio
from keyboards.default import menu_start
from keyboards.default.start_menu import menu_beck, menu_beck_inv
from loader import dp, bot


@dp.message_handler(text='🧙🏿Инвайт', state='*')
async def start(message: types.Message, state: FSMContext):
    proxy_file, sessions_len = create_array_account_proxy()
    __userid = message.from_user.id
    await message.answer(f"<b>👑{message.from_user.first_name}👑 Вы перешели в - 🧙🏿Инвайт</b>\n\n"
                         f"<b>Аккаунтов для инвайтинга -</b> <code>{len(sessions_len)}</code>\n"
                         f"<b>Прокси для инвайтинга -</b> <code>{len(proxy_file)}</code>\n\n"
                         f"Что бы начать инвайтить пришлите базу и ссылку\n"
                         f"Пример",reply_markup=menu_beck)

    file = InputFile(
        fr"data/spam_bd.csv"
    )
    await bot.send_document(chat_id=message.chat.id, document=file, caption="https://t.me/combain777bot", reply_markup=menu_beck)
    await state.set_state('invitedoc')

@dp.message_handler(state='invitedoc',content_types=['document'])
async def add_channel_get_photo(message, state: FSMContext):
    await message.document.download(rf'data/spam_bd.csv')
    #data = await state.get_data()
    await state.update_data(invitedoc=message.caption)
    await message.answer("Начинаем инвайтить пользователей?", reply_markup=menu_beck_inv)


@dp.message_handler(text='🚀 Инвайтим', state='*')
async def start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_invite = data['invitedoc']
    await message.answer('Инвайтинг начился', reply_markup=menu_beck)
    msg = await message.answer('Статус запущенно')
    pc = get_user_invaiter_tg_asyncio(chat_invite,msg=msg)

    await pc.__start__()
    await state.finish()