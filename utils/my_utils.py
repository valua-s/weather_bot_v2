from datetime import datetime

import pytz
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from keyboards.all_keyboards import main_kb

geolocator = Nominatim(user_agent="GetLoc")
tf = TimezoneFinder()


def create_time_zone(lat, lon):
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    return timezone_str


def create_url(lat, lon, period):
    """Функция формирования запроса к серверу."""
    if period == 'hourly':
        info = 'temperature_2m,precipitation'
        days = '2'
    else:
        info = 'temperature_2m_max,temperature_2m_min,precipitation_sum'
        days = '1'
    url = (f'https://api.open-meteo.com/v1/forecast?'
           f'latitude={lat}'
           f'&longitude={lon}'
           f'&{period}={info}&'
           f'timezone=auto&forecast_days={days}'
           f'&format=json')
    return url


def send_response(url):
    return requests.get(url).json()


def get_now_time():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    # Convert to naive datetime
    return now.replace(tzinfo=None)


def get_adress(lat, lon):
    location = geolocator.reverse(f"{lat},{lon}", language='ru')
    if location:
        full_adress = location.raw['address']
        if full_adress.get('city') is not None:
            return full_adress.get('city')
    return "Ошибка получения адреса"


def is_float(value):
    """Check if the string is a float."""
    try:
        return float(value)
    except ValueError:
        return None


def process_data(response, schedule_time):
    """Обработка полученного запроса.

    Составление словаря списков для таблицы.
    """
    hourly = response['hourly']
    hourly_temperature_2m = hourly['temperature_2m']
    hourly_precipitation = hourly['precipitation']
    start_list = int(schedule_time.split(':')[0])
    end_list = start_list + 12
    time_list = []
    for i in range(start_list, end_list):
        if i < 10:
            time_list.append('0' + str(i) + ':00')
        elif i < 24 and i > 9:
            time_list.append(str(i) + ':00')
        elif i > 24 and i < 34:
            time_list.append('0' + str(i-24) + ':00')
        else:
            time_list.append(str(i-24) + ':00')
    hourly_precipitation_list = hourly_precipitation[start_list: end_list]
    hourly_temperature_2m_list = hourly_temperature_2m[start_list: end_list]
    table = create_table(
                   time_list, hourly_temperature_2m_list,
                   hourly_precipitation_list)
    message = (f'Доброго времения суток!\n'
               f'Это твой ежедневный прогноз на сегодня\n'
               f'{table}\n'
               f'Хорошего дня тебе, человек!')
    return message


def create_table(list1, list2, list3):
    header = f"{'Время':<7} {'t °C':<8} {'Осадки %':<12}"
    separator = "-" * 30
    rows = [f"{str(a):<7} {str(b):<8} {str(c):<12}" for a, b, c in zip(
        list1, list2, list3)]
    table = "\n".join([header, separator] + rows)
    return table


def process_data_short_weather(response):
    daily = response['daily']
    max_temp = daily['temperature_2m_max']
    min_temp = daily['temperature_2m_min']
    precipitation_sum = daily['precipitation_sum']
    if precipitation_sum != 0.0:
        precipitation = 'Осадочки планируются!'
    else:
        precipitation = 'Осадочков не будет!'
    message = (f'А вот и погодка на сегодня! \n\n'
               f'Минимальная температура воздуха: {min_temp[0]}\n'
               f'Максимальная температура воздуха: {max_temp[0]}\n'
               f'{precipitation}\n\n'
               f'Хорошего дня тебе, человек!')
    return message


async def create_error_message(message):
    await message.answer(
                ('Возникли проблемки, попробуйте снова'
                 'или обратитесь в поддержку!'), reply_markup=main_kb()
            )


def create_table_forcasts(data):  # url, time, city
    message = ''
    text = ''
    if type(data) is list:
        value = data
        data = {}
        data[-1] = value
    for key, value in data.items():
        if 'daily' in value[0]:
            frequency = 'Краткий прогноз'
        else:
            frequency = 'Табличный прогноз'
        text += (f'{frequency} в '
                 f'{value[1]} в городе {value[2]} ')
        text += '\n'
        if key >= 0:
            text = (f'{key + 1}.') + text
            message += text
            text = ''
        else:
            message += text
    return message
