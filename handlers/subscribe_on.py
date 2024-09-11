from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.all_keyboards import (create_geo_kb, create_unsub_kb)

subscribe_on_router = Router()


@subscribe_on_router.message(F.text == '☀️ Составить прогноз')
async def cmd_forecast(message: Message):
    await message.answer(
        'Для начала передайте информацию о вашей Локации',
        reply_markup=create_geo_kb()
        )


@subscribe_on_router.message(Command('forcast'))
async def cmd_forecast_2(message: Message):
    await message.answer(
        'Для начала передайте информацию о вашей Локации',
        reply_markup=create_geo_kb()
        )


@subscribe_on_router.message(F.text == '🛑 Отменить подписку на прогноз')
async def cmd_cancel(message: Message):
    await message.answer(
        'Можете нажать кнопку, но она пока не работает 🤷',
        reply_markup=create_unsub_kb()
        )


@subscribe_on_router.message(Command('cancel'))
async def cmd_cancel_2(message: Message):
    await message.answer(
        'Можете нажать кнопку, но она пока не работает 🤷',
        reply_markup=create_unsub_kb()
        )
