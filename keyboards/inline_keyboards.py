from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def contacts_keyboard():
    inline_kb_list = [
        [InlineKeyboardButton(
            text="Хабр", url='https://habr.com/ru/users/valua-s/'
            )],
        [InlineKeyboardButton(
            text="Телеграм", url='tg://resolve?domain=valua_s'
            )],
        [InlineKeyboardButton(
            text="Почта", url="mailto:va1.34@yandex.ru"
            )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
