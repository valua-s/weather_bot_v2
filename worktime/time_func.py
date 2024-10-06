from create_bot import bot, scheduler
from db_handler.db_users import Schedule_url, get_all_elements
from utils.my_utils import (process_data, process_data_short_weather,
                            send_response)


async def send_scheduled_message(chat_id: int, message: str, bot=bot):
    await bot.send_message(chat_id, message)


async def create_list():
    records = await get_all_elements(Schedule_url)
    for record in records:
        schedule_time = record.schedule_time
        url = record.url
        timezone = record.time_zone
        hour = int(schedule_time.split(':')[0])
        minute = int(schedule_time.split(':')[1])
        if 'daily' in url:
            message = process_data_short_weather(send_response(url))
        else:
            message = process_data(send_response(url), schedule_time)
        id = record.user_telegram_id
        scheduler.add_job(
            send_scheduled_message,
            'cron', hour=hour, minute=minute,
            timezone=timezone,
            args=[int(id), message])
