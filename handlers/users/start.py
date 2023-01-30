import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu_start
from loader import dp



@dp.message_handler(text='🔙Назад', state='*')
@dp.message_handler(CommandStart(),state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    __userid = message.from_user.id
    await message.answer(f"<b>Приветствую 👑{message.from_user.first_name}👑</b>\n\n"
                         f"Выберите одну из функция из комплекса - <code>😈 трактор</code>",reply_markup=menu_start)
