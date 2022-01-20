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
		except exceptions.Error as e:
			logger.error(f'{self.user_id} removed with error: {e}')
			await db.duplicate_protection(self.user_id, remove=True)
			return
		except Exception as e:
			logger.error(f'{self.user_id} removed with error: {e}')
			await db.duplicate_protection(self.user_id, remove=True)
			raise e

if __name__ == '__main__':
	uid = "715407122"
	authkey = "SucW6ln%2fgKYnXC2jhnk7K9f%2bFycmx66pjLOHtuGi%2bGDP513zUy%2fzbNkvuV6CCOp%2fMup0k1J0l8%2fmK8FXy2bspZtSVE%2bmuf%2fgv5gUJJblyzy4Zzrn60Plm8sMS8B6%2buAwrEP1Af6eagTiDQ%2b99ibRWttF4eieNQUKg03pXT3XxHmtTff%2f3isbDp32OmTgEIqrwNAX2h6K%2fWKxJHbH%2bLn4X%2fEh5oILykdJ%2bw0TvlXq6e5KcjjkeXzUaoaw4zkV3Ip32TdMZSqvD6vslC4evmMK04OJfXTAyWNT%2bQhImrbtOohJHoXCP4WoNvvcazdKXyNnmQqhi%2f41JgDqHJ4B5e%2fHPe7EzHSnMk%2b1pfQIzzfQqp5PzEcZlDnXrYRpVh44EipOrA6Fu7G1yN01f4%2fyOk6zOi9tEzSTmJSU9ejG7aaf3JYZfX8UMnKYjmi%2fb1%2fHXFVG%2bF3r7JYmwCWPQCKWbQtJdF5EVQSnX0AmUPf50ro9%2fMDeI537OTGDdSiIAUVDeJkrrytaBIlYNlqocgQ8wXghuKakrpMn1ouky%2f7Le1M7etkoPPBCRv0D5G8VJe3VHJ%2fFN0ErmSM%2bAfOp7ElpmPu3eXZg%2b9zvH%2fjG4pYEaw7kd5VkIGMW2OPnbvdRfinoJ5BenH1Bagi1ZTnNnCE5oGXE5OxqQgH7n2Ex%2bqAkiLIAe6EGPgH%2bUVzyL1uaenwxf9oozL1Y8FPFDTtr62rnzB5O3YxV%2fG1Nbyc2V3g4%2beEXzHmOJyCGAj%2bQBsdQxs9QpFa2p8MzjUFYTKkBHcXrh%2fSt4ClKhsFLyu0F4CJ4mNvklVeM2%2bmJIWFAp0glH7divYspLNtjUMmnAw5H1Lafc3uRSw7wcW9UTaIlt9iCHLPynLPAnr%2bMfTSn5xemWOGiR%2fVyZ3mJ1qJ9YMvravdlgrR5UicDWozyTzef4oe849%2bFiDx3AsO7lMyJvvALqvNYiAFY%2fArs2qLmgG41c9kYkhbZ3mza9J79fmmMWpITqDGRncVaJP0OK%2fbUKNxwhI5asAGDlWaYJTYnNgmDwUs%2fjqAD%2fAKcpuCaPHxsOJi63b%2fAJm3qRWBUHwCnPGUcHowpGb4n0aMUgWP7e5g3%2b9qPijwJeGDjPbV4x2ttHhdXTcVfnz3aY%2fRd5OfubMApYoxvvG39oWNK251NUipm5X0JHrNR16vKy%2fyWOeeob1pF8cEB0%2fxulgbEriewbgNzrfveYMFw9FElqjUQ8rMdkqt%2fRR4FqacQmJpYVF6tFKxhSvb5V8o7UkmpI5g15kdPtl5PH06zgJBSrN%2beGuKD14cf%2b2v%2bIrCfT5VIyrYVzkfxt0GV8ThcsIJX9t4RgUQOknNpO78poqgm4IPWPLyYZeasR55B9g%3d%3d"
	