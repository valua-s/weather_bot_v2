from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot):
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='forcast', description='Составить прогноз'),
                BotCommand(command='cancel', description='Отмена подписки')]
                # BotCommand(command='start_3', description='Старт 3')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
