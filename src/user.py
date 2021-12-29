from src import decorators as dc, exceptions, database as db, parser
from collections import Counter
import re
import requests
import time

GLOBAL_LOOP: list = []
gacha_ids = ["100", "200", "301", "302"]


class User:
	@dc.errors_handler
	def __init__(self, link: str):
		self.link = str(link)
		try:
			self.authkey: str = re.search(r'(?<=authkey=)[^&#]+', self.link, flags=re.MULTILINE).group()
		except AttributeError:
			raise exceptions.AuthKeyMissedException
		self.__request_link = f'{parser.request_link_header}&lang=en&authkey={self.authkey}&gacha_type=200&size=1'
		self.__response = requests.get(self.__request_link).json()
		if self.__response["message"] == "OK":
			self.user_id = self.__response["data"]["list"][0]["uid"]
		else:
			raise exceptions.AuthKeyInvalidException(self.__response["message"])
		self.exist_before_assignment = db.check_user(user_id=self.user_id)
		print(time.asctime()+f' User {self.user_id} inited')
		
	@dc.errors_handler
	def delete_user(self):
		db.remove_user(user_id=self.user_id)
	
	async def __wish_iterator(self, gacha_id):
		end_id = ""
		dict_of_updates = Counter()
		last_item = db.get_last_wish(gacha_id, user_id=self.user_id) if self.exist_before_assignment else None
		while True:
			gacha_response: list = await parser.get_data(self.authkey, gacha_id, end_id)
			if len(gacha_response) == 0:
				break
			if last_item:
				items = [item for item in gacha_response if last_item < item["id"]]
				dict_of_updates.update(db.append_wish(items, user_id=self.user_id))
				if last_item in [item["id"] for item in gacha_response]:
					break
			else:
				dict_of_updates.update(db.append_wish(gacha_response, user_id=self.user_id))
			end_id = gacha_response[len(gacha_response) - 1]["id"]
		return dict_of_updates
		
	@dc.async_errors_handler
	async def start_update_db(self) -> dict:
		"""This method should start a DB update for current user"""
		if self.user_id in GLOBAL_LOOP:
			raise exceptions.DuplicateUserInLoop
		GLOBAL_LOOP.append(self.user_id)
		counter = Counter()
		start = {"100": 0, "200": 0, "301": 0, "302": 0, "400": 0}
		final = {}
		counter.update(start)
		try:
			if not self.exist_before_assignment:
				db.create_user(user_id=self.user_id)
			for gacha_id in gacha_ids:
				counter.update(await self.__wish_iterator(gacha_id))
			print(f'{self.user_id} removed')
			GLOBAL_LOOP.pop(GLOBAL_LOOP.index(self.user_id))
			final.update(counter)
			return final
		except Exception as e:
			print(f'{self.user_id} removed with error')
			GLOBAL_LOOP.pop(GLOBAL_LOOP.index(self.user_id))
			raise e
			