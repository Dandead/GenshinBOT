from src import user
import asyncio
import logging
from src.bot import bot

logging.basicConfig(
	level=logging.CRITICAL
)
# 	filename='log/wishes.log',
# 	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 	datefmt='%d-%b-%y %H:%M:%S'


asyncio.run(bot.main())
