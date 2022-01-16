import asyncio
import configparser
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from src.bot.handlers import base_handlers as bh, wishes_handler as wh

logger = logging.getLogger("bot")


async def set_base_commands(bot: Bot):
	commands = [
		types.BotCommand(command="/start", description="Запустить бота"),
		types.BotCommand(command="/cancel", description="Вернуться вначало")
	]
	await bot.set_my_commands(commands)


async def main():
	try:
		logger.error("Starting bot")
		config = configparser.ConfigParser()
		config.read('config/bot.ini')
		bot = Bot(**dict(config.items('telegram')))
		config.read('config/databases.ini')
		storage = RedisStorage2(**dict(config.items('REDIS_CACHE')))
		dp = Dispatcher(bot, storage=storage)
		bh.register_handlers_base(dp)
		wh.register_handlers_wishes(dp)
		
		await set_base_commands(bot)
		await dp.skip_updates()
		await dp.start_polling()
	finally:
		await dp.storage.close()
		await dp.storage.wait_closed()
		await bot.session.close()
		logger.error("Closing bot")

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		logger.error("Bot stopped!")
