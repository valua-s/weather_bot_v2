from aiogram import F, Router
from aiogram.types import Message

from keyboards.inline_keyboards import contacts_keyboard

contacts_router = Router()


@contacts_router.message(F.text == '✉️ Связаться с автором')
async def cmd_contacts(message: Message):
    await message.answer(
        'Контакты:',
        reply_markup=contacts_keyboard())
