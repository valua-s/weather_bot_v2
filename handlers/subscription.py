from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from create_bot import logger
from db_handler.db_users import (Schedule_url, create, delete,
                                 get_all_elements_for_user, get_element)
from handlers.start import cmd_come_back
from keyboards.all_keyboards import (create_data_correct_kb,
                                     create_delete_confirm_kb,
                                     create_delete_kb, create_final_changes_kb,
                                     create_geo_kb, create_one_more_kb,
                                     create_period_kb, create_unsub_kb,
                                     create_yes_no_city_kb,
                                     create_yes_no_data_kb, main_kb)
from utils.my_utils import (create_error_message, create_table_forcasts,
                            create_time_zone, create_url, get_adress, is_float)

subscribe_on_router = Router()


class Form(StatesGroup):
    lat = State()
    lon = State()
    period = State()
    schedule = State()
    city = State()
    data_forcasts = State()
    data_delete = State()


@subscribe_on_router.message(F.text == 'На главную')
@subscribe_on_router.message(Command('backhome'))
async def to_home(message: Message):
    await cmd_come_back(message)


async def cmd_ask_location(message: Message, state: FSMContext):
    await message.answer(
        'Передайте информацию о вашей Локации',
        reply_markup=create_geo_kb()
        )


@subscribe_on_router.message(F.text == '☀️ Составить прогноз')
@subscribe_on_router.message(Command('forcast'))
@subscribe_on_router.message(F.text == 'Изменить город')
async def insert_location(message: Message, state: FSMContext):
    await cmd_ask_location(message, state)
    await state.set_state(Form.lat)


@subscribe_on_router.message(F.location)
async def cmd_ask_city(message: Message, state: FSMContext):
    lat = message.location.latitude
    await state.update_data(lat=lat)
    lon = message.location.longitude
    await state.update_data(lon=lon)
    await create_adress_message(lat, lon, message, state)


async def create_adress_message(lat, lon, message: Message,
                                state: FSMContext):
    try:
        data = await state.get_data()
    except Exception as e:
        logger.error(f'Ошибка при получении данных из state: {e}')
        await create_error_message(message)
    location_city = get_adress(lat, lon)
    await state.update_data(city=location_city)
    if "Ошибка" not in location_city:
        await message.answer(
            f'Я определил ближайший к вам город. Это {location_city}?',
            reply_markup=create_yes_no_city_kb()
        )
        if not data.get('schedule'):
            await state.set_state(Form.period)
        else:
            await state.set_state(Form.schedule)
    else:
        text = ('Есть сложности с определением Вашей локации,\n'
                'хотите передать данные вручную?')
        await message.answer(text, reply_markup=create_yes_no_data_kb())


@subscribe_on_router.message(F.text == '📍 Отправить локацию вручную')
@subscribe_on_router.message(F.text == 'Да, я передам данные вручную')
@subscribe_on_router.message(F.text == ("Нет, мой город другой, я передам "
                             "локацию еще раз"))
async def cmd_ask_lat_city(message: Message, state: FSMContext):
    await state.set_state(Form.lat)
    await message.answer('Введите широту:')


@subscribe_on_router.message(F.text, Form.lon)
async def cmd_ask_manualy_input_city(message: Message, state: FSMContext):
    lon = is_float(message.text)
    if lon:
        await state.update_data(lon=lon)
        data = await state.get_data()
        lat = data.get('lat')
        await create_adress_message(lat, lon, message, state)


@subscribe_on_router.message(F.text, Form.lat)
async def cmd_ask_lon_city(message: Message, state: FSMContext):
    lat = is_float(message.text)
    if lat:
        await state.update_data(lat=lat)
        await state.set_state(Form.lon)
        await message.answer('Введите долготу:')
    else:
        await message.answer('Введенные данные не валидны,'
                             'попробуйте еще раз или вернитесь на главную'
                             'через команду в меню  👇')
        await cmd_ask_lat_city(message, state)


@subscribe_on_router.message(F.text == "Да, это так", Form.period)
@subscribe_on_router.message(F.text == "Изменить график прогноза")
async def choose_period(message: Message, state: FSMContext):
    await message.answer(
            'Выберите из двух вариантов подписки',
            reply_markup=create_period_kb()
        )


@subscribe_on_router.message(F.text == "Да, это так", Form.schedule)
async def return_to_summary(message: Message, state: State):
    data = await state.get_data()
    await show_summary(message, data)


@subscribe_on_router.message(F.text == 'Подробный прогноз в виде таблицы')
async def install_period_current(message: Message, state: FSMContext):
    await state.update_data(period='hourly')
    schedule = await state.get_data()
    if not schedule.get('schedule'):
        await choose_time(message=message, state=state)
    else:
        await return_to_summary(message, state)


@subscribe_on_router.message(F.text == "Краткий прогноз")
async def install_period_daily(message: Message, state: FSMContext):
    await state.update_data(period='daily')
    schedule = await state.get_data()
    if not schedule.get('schedule'):
        await choose_time(message=message, state=state)
    else:
        await return_to_summary(message, state)


@subscribe_on_router.message(F.text == "Изменить время уведомлений")
async def choose_time(message: Message, state: FSMContext):
    await state.set_state(Form.schedule)
    await message.answer(
        'Введите время в которое хотите получать уведомления \n'
        '(Местное время вашего города в формате ЧЧ:ММ)')


@subscribe_on_router.message(F.text.contains(':'),
                             Form.schedule)
async def form_information(message: Message, state: FSMContext):
    if message.text.__contains__(':'):
        data = await state.update_data(schedule=message.text)
    else:
        data = await state.get_data()
    await show_summary(message=message, data=data)


@subscribe_on_router.message(F.text.regexp(r"^(\d+).*"), Form.schedule)
@subscribe_on_router.message(F.text.regexp(r"^(\d+).*"), Form.period)
async def error_time_information(message: Message, state: FSMContext):
    await message.answer(
        'Не тот формат, друг мой, повторите попытку \n'
        'или вернитесь в главное меню, командой')
    await choose_time(message, state)


@subscribe_on_router.message(F.text == "Думаю, что ничего не буду менять")
async def nothing_to_change(message: Message, state: FSMContext):
    await message.answer(
        'Верное решение, раз уж решили \n'
        'то надо идти до конца 💪🏻')
    await form_information(message, state)


async def show_summary(message: Message, data):
    period = data.get('period')
    schedule = data.get('schedule')
    adress = data.get('city')
    if period == 'daily':
        period = 'кратком прогнозе'
    else:
        period = 'подробном прогнозе в виде таблицы'
    text = (
        f'Давайте перепроверим введенные данные:\n'
        f'Вы будете получать уведомления каждый день в {schedule}\n'
        f'о {period} в городе {adress}\n'
        f'Все верно?\n'
    )
    await message.answer(text, reply_markup=create_data_correct_kb())


async def create_data_from_state(message, state):
    """Создает словарь для БД."""
    data = await state.get_data()
    lat = data.get('lat')
    lon = data.get('lon')
    user_telegram_id = message.from_user.id
    url = create_url(lat, lon, data.get('period'))
    time_zone = create_time_zone(lat, lon)
    city = data.get('city')
    schedule_url_data = {
        'user_telegram_id': user_telegram_id,
        'url': url,
        'time_zone': time_zone,
        'schedule_time': data.get('schedule'),
        'city': city
    }
    return schedule_url_data


@subscribe_on_router.message(F.text == "Да, введенные данные верны",
                             Form.schedule)
@subscribe_on_router.message(F.text == "Да, я хочу добавить еще один",
                             Form.schedule)
async def create_schedule(message: Message, state: FSMContext):
    schedule_url_data = await create_data_from_state(message, state)
    await message.answer(
                'Друг мой, создаю для тебя прогноз, ожидай минутку!'
            )
    try:
        result = await get_element(Schedule_url, message.from_user.id)
        if not result or message.text == "Да, я хочу добавить еще один":
            await create(Schedule_url, schedule_url_data)
            await message.answer(
                'Успешное добавление расписания, ждите прогноза!',
                reply_markup=main_kb(message.from_user.id)
            )
            await state.clear()
        else:
            await message.answer(
                'Для Вас уже создан прогноз, хотите добавить еще один?',
                reply_markup=create_one_more_kb()
            )
    except Exception as e:
        logger.error(f'Ошибка при добавлении данных прогноза: {e}')
        await create_error_message(message)


@subscribe_on_router.message(F.text == "Нет, я хочу поменять информацию",
                             Form.schedule)
async def create_change_schedule(message: Message, state: FSMContext):
    await message.answer('Выберите к какому шагу вернуться',
                         reply_markup=create_final_changes_kb())


@subscribe_on_router.message(F.text == '🛑 Отменить подписку на прогноз')
@subscribe_on_router.message(Command('cancel'))
async def cmd_cancel(message: Message):
    await message.answer(
        'Очень жаль отменять подписку, нужно подтверждение 🤷',
        reply_markup=create_unsub_kb()
        )


@subscribe_on_router.message(F.text == 'Я хочу отменить подписку на прогноз')
async def cmd_cancel_conf(message: Message, state: FSMContext):
    await message.answer('Друг мой, минутку, я ищу твои подписки')
    try:
        forcasts = await get_all_elements_for_user(
            Schedule_url, message.from_user.id)
        if forcasts:
            count = len(forcasts)
            await message.answer('Друг мой, выбери прогноз из списка',
                                 reply_markup=create_delete_kb(count))
            data = {}
            for i in range(count):
                data[i] = [forcasts[i].url, forcasts[i].schedule_time,
                           forcasts[i].city]
            await state.update_data(data_forcasts=data)
            await state.set_state(Form.data_forcasts)
            await message.answer(create_table_forcasts(data))
    except Exception as e:
        logger.error(e)
        await message.answer('Вы еще не создавали проноз',
                             reply_markup=main_kb(message.from_user.id))


@subscribe_on_router.message(F.text.regexp(r"[0-9]"),
                             Form.data_forcasts)
async def delete_this_question(message: Message, state: FSMContext):
    num_of_forcast = int(message.text)
    data = await state.get_data()
    forcast_info = data.get('data_forcasts')[num_of_forcast-1]
    await message.answer('Подтвердите удаление этого прогноза:')
    await message.answer(create_table_forcasts(forcast_info),
                         reply_markup=create_delete_confirm_kb())
    await state.update_data(data_delete=forcast_info)
    await state.set_state(Form.data_delete)


@subscribe_on_router.message(F.text == 'Да, пусть горит синим пламенем',
                             Form.data_delete)
async def delete_this_action(message: Message, state: FSMContext):
    await message.answer('Минутку ожидания, сжигаю все мосты')
    data = await state.get_data()
    data_delete = data.get('data_delete')
    try:
        await delete(Schedule_url, message.from_user.id,
                     data_delete[0])
    except Exception as e:
        logger.error(e)
        await message.answer('Вы еще не создавали проноз',
                             reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer('Прогноз успешно удален',
                             reply_markup=main_kb(message.from_user.id))


@subscribe_on_router.message(F.text == 'Нет, это случайность',
                             Form.data_delete)
async def to_main(message: Message, state: FSMContext):
    await message.answer('Возвращаю тебя друг мой, в главное меню')
    await cmd_come_back(message)


@subscribe_on_router.message(F.text.regexp(r"[^0-9]"))
async def universal_answer(message: Message):
    await message.answer('Неизвестная мне команда, '
                         'я не придумал, что ответить 🙀 '
                         'но Вы можете предложить это моему хозяину')
