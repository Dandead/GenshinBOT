import aiohttp.client
import decorators as dc
from decorators import GLOBAL_LOOP
import re
import logging
import asyncio
import requests
import time
import exceptions
import hashlib

# TODO:
#  Add __del__ in User
#  Add normal logging



logging.basicConfig(
# 	filename='log/wishes.log',
	level=logging.CRITICAL
# 	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 	datefmt='%d-%b-%y %H:%M:%S'
)
# wish_logger = logging.getLogger(__name__)
# wish_logger.setLevel(logging.INFO)


@dc.errors_handler
class User:
	def __init__(self, link: str):
		self.link = str(link)
		self.gacha_ids = ["100", "200", "301", "302"]
		self.request_link_header = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1"
		self.set_user_info()
		self.exist_before_assignment = self.__check_user()
		print(time.asctime()+f' User {self.user_id} inited')
		
	def set_user_info(self):
		try:
			self.authkey: str = re.search(r'(?<=authkey=)[^&#]+', self.link, flags=re.MULTILINE).group()
		except AttributeError:
			raise exceptions.AuthKeyMissedException
		self.request_link = f'{self.request_link_header}&lang=en&authkey={self.authkey}&gacha_type=200&size=1'
		self.response = requests.get(self.request_link).json()
		if self.response["message"] == "OK":
			self.user_id = self.response["data"]["list"][0]["uid"]
		else:
			raise exceptions.AuthKeyInvalidException(self.response["message"])
	
	async def get_data(self, link_return: bool = None, gacha_id: str = "200", end_id: str = None):
		"""Must return lists of wishes data/only one list/link to json"""
		self.request_link = f'{self.request_link_header}&lang=en&authkey={self.authkey}&gacha_type={gacha_id}&size=20&end_id={end_id}'
		if link_return:
			return self.request_link
		async with aiohttp.ClientSession().get(self.request_link) as resp:
			self.response = await resp.json()
		if self.response["message"] == "OK":
			return self.response["data"]["list"]
		else:
			raise exceptions.AuthKeyInvalidException(self.response["message"])
	
	@dc.db_connect_decorator
	def __check_user(self, **kwargs) -> bool:
		"""Must return bool of existing user in DB."""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(f'SELECT * FROM usr WHERE uid = "{self.user_id}"')
		row = cursor.fetchone()
		if row:
			return True
		else:
			return False
	
	@dc.db_connect_decorator
	def __create_user(self, **kwargs):
		"""Must append user's info string into DB."""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(
			f'INSERT INTO `usr` '
			f'VALUES ("{self.user_id}","en","{self.authkey}")')
		print(f'User {self.user_id} created in DB')
	
	@dc.db_connect_decorator
	def remove_user(self, **kwargs):
		"""Must remove user from DB"""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(
			f'DELETE FROM `usr` '
			f'WHERE uid = "{self.user_id}"')
		print(time.asctime()+f' User {self.user_id} removed from DB')
	
	@dc.db_connect_decorator
	def __get_last_wish(self, gacha_id, **kwargs):
		"""Must return dict with user's last wish from table"""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		cursor.execute(
			f'SELECT MAX(id) '
			f'FROM `{gacha_id}` '
			f'WHERE uid="{self.user_id}"'
		)
		row = cursor.fetchone()
		if row["MAX(id)"]:
			return row["MAX(id)"]
		else:
			return None
	
	@dc.db_connect_decorator
	def __append_wish(self, items, gacha_id, **kwargs):
		"""Must append row with new item to DB"""
		cursor = kwargs.pop("conn").cursor(dictionary=True)
		if len(items) == 0:
			return
		for item in items:
			try:
				cursor.execute(
					f'INSERT INTO `{gacha_id}` '
					f'VALUES ("{self.user_id}","{item["time"]}","{item["name"]}","{item["item_type"]}","{item["rank_type"]}","{item["id"]}");'
				)
			except Exception as e:
				print(f'__append_wish method: {e}')
				return None
	
	async def __wish_iterator(self, gacha_id):
		end_id = ""
		count = 0
		last_item = self.__get_last_wish(gacha_id) if self.exist_before_assignment else None
		while True:
			gacha_response: list = await self.get_data(gacha_id=gacha_id, end_id=end_id)
			if len(gacha_response) == 0:
				break
			if last_item:
				items = [item for item in gacha_response if last_item < item["id"]]
				self.__append_wish(items, gacha_id)
				count+=len(items)
				if last_item in [item["id"] for item in gacha_response]:
					break
			else:
				self.__append_wish(gacha_response, gacha_id)
				count += len(gacha_response)
			end_id = gacha_response[len(gacha_response) - 1]["id"]
		print(time.asctime()+f' Added {count} new rows to "{gacha_id}" table for "{self.user_id}"')
	
	async def start_update_db(self):
		"""This method should start a DB update for current user"""
		self.shahash = hashlib.sha3_224(self.authkey.encode()).hexdigest()
		if self.shahash in GLOBAL_LOOP:
			print(123)
			raise exceptions.DuplicateUserInLoop()
		GLOBAL_LOOP.append(self.shahash)
		try:
			if not self.exist_before_assignment:
				self.__create_user()
			for gacha_id in self.gacha_ids:
				# asyncio.ensure_future(self.__wish_iterator(gacha_id))
				await self.__wish_iterator(gacha_id)
			print(f'{self.user_id} removed')
			GLOBAL_LOOP.pop(GLOBAL_LOOP.index(self.shahash))
		except Exception as e:
			print(f'{self.user_id} removed with error')
			GLOBAL_LOOP.pop(GLOBAL_LOOP.index(self.shahash))
			raise e
			