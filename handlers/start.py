from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from create_bot import logger
from db_handler.db_users import User, create, get_element
from keyboards.all_keyboards import main_kb
from utils.my_utils import get_now_time

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    full_name = user.first_name
    await message.answer(
        f'Добро пожаловать, {full_name}!\n'
        'Давайте составим для Вас прогноз погоды?',
        reply_markup=main_kb(user.id))
    if user.last_name:
        full_name += user.last_name
    data = {
        'user_telegram_id': user.id,
        'user_login': user.username,
        'full_name': full_name,
        'date_reg': get_now_time()
    }
    try:
        if not await get_element(User, user.id):
            await create(User, data)
    except ValueError:
        logger.error(f'Пользователь {full_name} {user.id}'
                     'не добавлен в базу данных.'
                     'Есть проблемы с данными.')
    except Exception as e:
        logger.error(f'Ошибка при добавлении пользователя: {e}')
    else:
        logger.info(f'Пользователь {full_name}'
                    f'с ID {user.id} добавлен в базу данных.')


@start_router.message(F.text == 'На главную')
@start_router.message(Command('backhome'))
@start_router.callback_query(F.data == 'back_home')
async def cmd_come_back(message: Message):
    await message.answer(
        'C возвращением! Выберите параметры из меню',
        reply_markup=main_kb(message.from_user.id))
