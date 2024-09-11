from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup,
                           )
from create_bot import admins
# from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb(user_telegram_id: int):
    """Создание базовой клавиатуры."""
    kb_list = [
        [KeyboardButton(text="✉️ Связаться с автором"),
         KeyboardButton(text="☀️ Составить прогноз")],
        [KeyboardButton(text="🛑 Отменить подписку на прогноз"),
         KeyboardButton(text="📖 О проекте")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
        )
    return keyboard


def create_geo_kb():
    """Создание кнопки отправить геолокацию"""
    kb_list = [
        [KeyboardButton(
            text="📍 Отправить геолокацию",
            request_location=True)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, передайте данные:")
    return keyboard


def create_unsub_kb():
    """Создание кнопки отмены подписки"""
    kb_list = [
        [KeyboardButton(text="🛑 Отмена подписки(пока не работает 🤷)")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard
