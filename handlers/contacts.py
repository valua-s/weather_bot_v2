from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from handlers.start import cmd_come_back
from keyboards.all_keyboards import main_kb
from keyboards.inline_keyboards import contacts_keyboard

contacts_router = Router()


@contacts_router.message(F.text == 'На главную')
@contacts_router.message(Command('backhome'))
async def return_to_home(message: Message):
    await cmd_come_back(message)


@contacts_router.message(F.text == '✉️ Связаться с автором')
async def cmd_contacts(message: Message):
    await message.answer(
        'Контакты:',
        reply_markup=contacts_keyboard())


@contacts_router.message(F.text == '📖 О проекте')
async def cmd_about(message: Message):
    await message.answer(
        ('Этот проект создан при поддержке меня, и снова меня \n'
         'еще конечно сильно поучаствовал чат GPT, и \n'
         '@yakovenkoalex by Habr, так как создал ряд постов по созданию \n'
         'чем и вдохновил меня на создание сего чуда и творения моей души \n'
         '\n'
         'Немного полезной информации: в этом боте можно составить себе \n'
         'прогноз погоды, который будет приходить в определенное время, \n'
         'в выбранном городе, можно составить несколько прогнозов для \n'
         'разных городов или времени. Прогноз будет приходить каждый день \n'
         'и радовать теплыми пожеланиями!'),
        reply_markup=main_kb(message.from_user.id))
