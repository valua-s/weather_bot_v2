from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.all_keyboards import (main_kb)


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Добро пожаловать! Давайте составим для Вас прогноз погоды?',
        reply_markup=main_kb(message.from_user.id))
    # здесь получаем ID пользователя, когда он присылает нам команду


@start_router.message(F.text == 'На главную')
async def cmd_come_back(message: Message):
    await message.answer(
        'C возвращением! Выберите параметры из меню',
        reply_markup=main_kb(message.from_user.id))


@start_router.message(Command('backhome'))
async def cmd_backhome(message: Message):
    await message.answer(
        'C возвращением! Выберите параметры из меню',
        reply_markup=main_kb(message.from_user.id))


@start_router.callback_query(F.data == 'back_home')
async def cmd_back_home(call: CallbackQuery):
    await call.message.answer(
        'C возвращением! Выберите параметры из меню',
        reply_markup=main_kb(call.message.from_user.id))
