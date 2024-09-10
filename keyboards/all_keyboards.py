from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup)
from create_bot import admins
# from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb(user_telegram_id: int):
    """Создание базовой клавиатуры."""
    kb_list = [
        [KeyboardButton(text="📖 О проекте"),
         KeyboardButton(text="☀️ Составить прогноз")],
        [KeyboardButton(text="🛑 Отменить подписку на прогноз"),]
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
    kb_list = [
        [KeyboardButton(text="🛑 Отмена подписки(пока не работает 🤷)")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


# def create_spec_kb():
#     """Создание клавиатуры со специальными кнопками."""
#     kb_list = [
#         [KeyboardButton(text="Отправить гео",
#                         request_location=True)],
#         [KeyboardButton(text="Поделиться номером",
#                         request_contact=True)],
#         [KeyboardButton(text="Отправить викторину/опрос",
#                         request_poll=KeyboardButtonPollType())]
#     ]
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=kb_list,
#         resize_keyboard=True,
#         one_time_keyboard=True,
#         input_field_placeholder="Пожалуйста, передайте данные:")
#     return keyboard


# def create_rat():
#     """Создание выравнивания кнопок клавиатуры."""
#     builder = ReplyKeyboardBuilder()
#     for item in [str(i) for i in range(1, 11)]:
#         builder.button(text=item)
#     builder.button(text='Назад')
#     builder.adjust(4, 4, 2, 1)
#     return builder.as_markup(resize_keyboard=True)
