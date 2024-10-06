from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def contacts_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(
            text='Хабр', url='https://habr.com/ru/users/valua-s/'
            )],
        [InlineKeyboardButton(
            text='Телеграм', url='tg://resolve?domain=valua_s'
            )],
        [InlineKeyboardButton(
            text='На главную', callback_data='back_home'
            )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
