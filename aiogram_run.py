import asyncio

# from work_time.time_func import send_time_msg
from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp, scheduler
from handlers.contacts import contacts_router
from handlers.start import start_router
from handlers.subscription import subscribe_on_router
from worktime.time_func import create_list


async def set_commands(bot):
    commands = [BotCommand(command='backhome', description='На главную'),
                BotCommand(command='forcast', description='Составить прогноз'),
                BotCommand(command='cancel', description='Отмена подписки')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands(bot)


async def main():
    # регистрация роутеров
    dp.include_router(contacts_router)
    dp.include_router(start_router)
    dp.include_router(subscribe_on_router)
    dp.startup.register(start_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        scheduler.start()
        await create_list()
        await dp.start_polling(
                bot, allowed_updates=dp.resolve_used_update_types())

    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
