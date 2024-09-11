from aiogram import Router, F
from aiogram.filters import CommandObject
from aiogram.types import Message
from keyboards.all_keyboards import (create_geo_kb, create_unsub_kb)

subscribe_on_router = Router()


@subscribe_on_router.message(F.text == 'Составить прогноз')
async def cmd_forecast(message: Message):
    await message.answer(
        'Для начала передайте информацию о вашей Локации',
        reply_markup=create_geo_kb()
        )


@subscribe_on_router.message(F.text == 'Отменить подписку на прогноз')
async def cmd_cancel(message: Message):
    await message.answer(
        'Я пока не работаю, но буду отменять подписку',
        reply_markup=create_unsub_kb()
        )
