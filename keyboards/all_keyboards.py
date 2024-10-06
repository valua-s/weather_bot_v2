from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from create_bot import admins

# from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb(user_telegram_id: int):
    """Создание стартовой клавиатуры."""
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
            text="📍 Отправить геолокацию (только с мобильных устройств)",
            request_location=True),
         KeyboardButton(
            text="📍 Отправить локацию вручную")]
        ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, передайте данные:")
    return keyboard


def create_unsub_kb():
    """Создание кнопки отмены подписки"""
    kb_list = [
        [KeyboardButton(text="Я хочу отменить подписку на прогноз"),
         KeyboardButton(text="На главную")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_yes_no_city_kb():
    kb_list = [
        [KeyboardButton(text="Да, это так"),
         KeyboardButton(text=("Нет, мой город другой, я передам локацию "
                        "еще раз"))]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_yes_no_data_kb():
    kb_list = [
        [KeyboardButton(text="Да, я передам данные вручную"),
         KeyboardButton(text="На главную")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_period_kb():
    kb_list = [
        [KeyboardButton(text="Подробный прогноз в виде таблицы"),
         KeyboardButton(text="Краткий прогноз")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_data_correct_kb():
    kb_list = [
        [KeyboardButton(text="Да, введенные данные верны"),
         KeyboardButton(text="Нет, я хочу поменять информацию")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_final_changes_kb():
    kb_list = [
        [KeyboardButton(text="Изменить город"),
         KeyboardButton(text="Изменить график прогноза")],
        [KeyboardButton(text="Изменить время уведомлений"),
         KeyboardButton(text="Думаю, что ничего не буду менять")],
        [KeyboardButton(text="На главную")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_one_more_kb():
    kb_list = [
        [KeyboardButton(text="Да, я хочу добавить еще один"),
         KeyboardButton(text="Нет, я совсем забыл(а) об этом")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_delete_kb(count):
    kb_list = []
    for i in range(count):
        kb_list.append([KeyboardButton(text=str(i + 1))])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard


def create_delete_confirm_kb():
    kb_list = [
        [KeyboardButton(text="Да, пусть горит синим пламенем"),
         KeyboardButton(text="Нет, это случайность")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Пожалуйста, выберите из меню:")
    return keyboard
