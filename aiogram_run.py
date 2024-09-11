import asyncio

from create_bot import bot, dp  # , scheduler
from handlers.start import start_router
# from work_time.time_func import send_time_msg
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='forcast', description='Составить прогноз'),
                BotCommand(command='cancel', description='Отмена подписки')]
                # BotCommand(command='start_3', description='Старт 3')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands(bot)


async def main():
    # регистрация роутеров
    dp.include_router(start_router)
    dp.startup.register(start_bot)
    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
