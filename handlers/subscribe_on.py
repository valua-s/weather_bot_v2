from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.all_keyboards import (create_geo_kb, create_unsub_kb)

start_router = Router()


@start_router.message(Command('☀️ Составить прогноз'))
async def cmd_forecast(message: Message):
    await message.answer(
        'Для начала передайте информацию о вашей Локации',
        reply_markup=create_geo_kb(message.from_user.id)
        )


@start_router.message(Command('🛑 Отменить подписку на прогноз'))
async def cmd_cancel(message: Message):
    await message.answer(
        'Я пока не работаю, но буду отменять подписку',
        reply_markup=create_unsub_kb(message.from_user.id)
        )
