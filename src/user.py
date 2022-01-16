import logging
from src import exceptions, database as db, parser
from collections import Counter
import re

logger = logging.getLogger("bot")


class User:
	def __init__(self, link: str = None, uid: str = None, authkey: str = None):
		self.user_id = uid
		self.authkey = authkey
		if link:
			self.link = str(link)
			try:
				self.authkey: str = re.search(r'(?<=authkey=)[^&#]+', self.link, flags=re.MULTILINE).group()
			except AttributeError:
				raise exceptions.AuthKeyMissedException
			self.user_id = parser.get_uid(self.authkey)
		self.exist_before_assignment = db.check_user(self.user_id)
		# logger.info(f' User {self.user_id} inited')
		
	def delete_user(self):
		db.remove_user(user_id=self.user_id)
	
	async def __wish_iterator(self, gacha_id):
		end_id = ""
		list_of_updates: dict = Counter()
		last_item: str = db.get_last_wish(self.user_id, gacha_id)
		while True:
			gacha_response: list = await parser.async_get_data(self.authkey, gacha_id, end_id)
			if len(gacha_response) == 0:
				break
			if last_item:
				items: list = [
					item
					for item in gacha_response
					if item.get("id") > last_item
				]
				updates = db.append_wish(items)
				list_of_updates.update(updates)
				if last_item in [item.get("id") for item in gacha_response]:
					break
			else:
				updates = db.append_wish(gacha_response)
				list_of_updates.update(updates)
			end_id = gacha_response[-1].get("id")
		return list_of_updates
		
	async def start_update_db(self) -> dict:
		"""This method should start a DB update for current user"""
		if not self.authkey:
			raise exceptions.AuthKeyMissedException
		if await db.duplicate_protection(self.user_id, check=True):
			raise exceptions.DuplicateUserInLoop
		await db.duplicate_protection(self.user_id)
		counter = Counter({"100": 0, "200": 0, "301": 0, "302": 0, "400": 0})
		try:
			if not self.exist_before_assignment:
				db.create_user(self.user_id)
			for gacha_id in ["100", "200", "301", "302"]:
				counter.update(await self.__wish_iterator(gacha_id))
			await db.duplicate_protection(self.user_id, remove=True)
			return counter
		except Exception as e:
			logger.info(f'{self.user_id} removed with error {e}')
			await db.duplicate_protection(self.user_id, remove=True)
			raise e
			