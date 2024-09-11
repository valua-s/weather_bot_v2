from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.all_keyboards import (main_kb, create_geo_kb, create_unsub_kb)


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Добро пожаловать! Давайте составим для Вас прогноз погоды?',
        reply_markup=main_kb(message.from_user.id))
    # здесь получаем ID пользователя, когда он присылает нам команду


@start_router.message(F.text == '/forcast')
async def cmd_forcast(message: Message):
    await message.answer('Push button forcast', reply_markup=create_geo_kb())


@start_router.message(Command('cancel'))
async def cmd_start_2(message: Message):
    await message.answer('Это ответ от нажатия кнопки отмены',
                         reply_markup=create_unsub_kb())

# @start_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     await message.answer(
#         'Запуск сообщения по команде /start_3'
#         'используя магический фильтр F.text!',
#         reply_markup=create_rat(message.from_user.id)
#         )
