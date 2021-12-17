from wishes import User
import asyncio
import time
import aiofiles


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
		await asyncio.sleep(10)
		print(time.asctime()+" New iteration")

asyncio.run(main())
