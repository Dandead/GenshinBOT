from wishes import User
import asyncio
import hashlib
import time


async def main():
	while True:
		with open("./config/curent_link.txt", "r") as e:
			lines = e.readlines()
		# with open("./config/curent_link.txt", "w"):
		# 	pass
		if lines:
			coro = []
			for line in lines:
				md5 = hashlib.sha3_224(line.encode()).hexdigest()
				# print(md5)
				new = User(md5, line)
				if new:
					coro.append(new.start_update_db())
			await asyncio.gather(*coro)
		await asyncio.sleep(5)
		print(time.asctime()+" New iteration")
	
asyncio.run(main())
