from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb_list = [
        [KeyboardButton(text=""),
         KeyboardButton(text="")],
        [KeyboardButton(text=""),]
    ]
def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="📖 О проекте", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="☀️ Составить прогноз", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="🛑 Отменить подписку на прогноз", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)