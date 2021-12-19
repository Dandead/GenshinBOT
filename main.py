from wishes import User
import asyncio
import telegram
import time
import aiofiles
from decorators import GLOBAL_LOOP


async def main():
	while True:
		async with aiofiles.open("./config/curent_link.txt", "r") as e:
			lines = await e.readlines()
		# with open("./config/curent_link.txt", "w"):
		# 	pass
		if lines:
			for line in lines:
				new = User(line)
				if new:
					asyncio.ensure_future(new.start_update_db())
					# await new.start_update_db()
				print(GLOBAL_LOOP)
				await asyncio.sleep(2)
		# await asyncio.sleep(15)
		print(time.asctime()+" New iteration")

asyncio.run(main())
