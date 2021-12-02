import aiohttp
from database_usage import *
import re
import logging
import asyncio
import time


logging.basicConfig(
	filename='log/wishes.log',
	level=logging.INFO,
	format='%(asctime)s - %(message)s',
	datefmt='%d-%b-%y %H:%M:%S'
)


class User:
	def __init__(self, link):
		self.link = str(link)
		self.gacha_ids = ["100", "200", "301", "302"]
		self.authkey: str = re.search(r'(?<=authkey=)[^&#]+', self.link, flags=re.MULTILINE).group()
		self.request_link_header = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1"
		self.user_id = asyncio.run(self.get_data())[0]["uid"]
		self.exist_before_assignment = self.check_user()
		
	async def get_data(self, link_return: bool=None, gacha_id: str=None, end_id: str=None):
		"""Must return lists of wishes data/only one list/authkey/link to json"""
		if self.authkey and gacha_id and end_id:
			self.request_link = f'{self.request_link_header}&lang=en&authkey={self.authkey}&gacha_type={gacha_id}&size=20&end_id={end_id}'
		elif self.authkey and not gacha_id and not end_id:
			self.request_link = f'{self.request_link_header}&lang=en&authkey={self.authkey}&gacha_type=200&size=1'
		else:
			raise ValueError
		if link_return:
			return self.request_link
		async with aiohttp.ClientSession().get(self.request_link) as resp:
			self.response = await resp.json()
		if self.response["message"] == "OK":
			return self.response["data"]["list"]
		else:
			raise ValueError
	
	@db_connect_decorator
	def check_user(self, **kwargs) -> bool:
		"""Must return bool of existing user in DB."""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(f'SELECT * FROM usr WHERE uid = "{self.user_id}"')
		row = cursor.fetchone()
		if row is not None:
			return True
		else:
			return False

	@db_connect_decorator
	def __create_user(self, **kwargs):
		"""Must append user's info string into DB."""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(
			f'INSERT INTO `usr` '
			f'VALUES ("{kwargs["uid"]}","en","{self.authkey}")')
		logging.info(f'User {kwargs["uid"]} created in DB')














		
	async def append_wish(self, gacha_id):
		end_id = ""
		count = 0
		while True:
			response: list = await self.get_data(gacha_id=gacha_id, end_id=end_id)
			print(f'{gacha_id} - {end_id}')
			count += len(response)
			if len(response) == 0:
				break
			end_id = response[len(response)-1]["id"]
		print(count)
	
	async def main(self):
		start_time = time.time()
		self.coros = []
		for gacha_id in self.gacha_ids:
			self.coros.append(self.append_wish(gacha_id))
		end_time = time.time()
		await asyncio.gather(*self.coros)
		print(f'All data was explored by {end_time-start_time} seconds')
		# return f'All data was explored by {end_time-start_time} seconds'
