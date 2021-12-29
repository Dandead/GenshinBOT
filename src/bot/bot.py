from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.bot.handlers import wishes_handler as wh, base_handlers as bh
import configparser
import asyncio


async def set_base_commands(bot: Bot):
	commands = [
		types.BotCommand(command="/start", description="Запустить бота"),
		types.BotCommand(command="/cancel", description="Вернуться вначало")
	]
	await bot.set_my_commands(commands)


async def main():
	config = configparser.ConfigParser()
	config.read('./config/bot.ini')
	bot = Bot(**dict(config.items('telegram')))
	dp = Dispatcher(bot, storage=MemoryStorage())
	wh.register_handlers_wishes(dp)
	bh.register_handlers_base(dp)
	
	await set_base_commands(bot)
	await dp.skip_updates()
	await dp.start_polling()

if __name__ == "__main__":
	asyncio.run(main())
