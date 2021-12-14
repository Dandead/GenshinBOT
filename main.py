from wishes import User
import asyncio
import hashlib


GLOBAL_LOOP = []


async def main():
	while True:
		with open("./config/curent_link.txt", "r") as e:
			lines = e.readlines()
		with open("./config/curent_link.txt", "w") as r:
			pass
		if lines:
			coro = []
			for line in lines:
				md5 = hashlib.sha3_224(line.encode()).hexdigest()
				print(md5)
				new = User(md5, line)
				coro.append(new.start_update_db())
			await asyncio.gather(*coro)
		await asyncio.sleep(5)
		print("new iteration")
	
asyncio.run(main())
