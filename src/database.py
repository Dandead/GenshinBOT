import src.decorators as dc
from collections import Counter
import time


@dc.wishes_db_conn
def check_user(**kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM usr WHERE uid = "{kwargs.get("user_id")}"')
	row = cursor.fetchone()
	if row:
		return True
	else:
		return False


@dc.wishes_db_conn
def create_user(**kwargs):
	"""Must append user's info string into DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'INSERT INTO `usr` '
		f'VALUES ("{kwargs.get("user_id")}","en","{kwargs.get("authkey")}")')
	print(f'User {kwargs.get("user_id")} created in DB')


@dc.wishes_db_conn
def remove_user(**kwargs):
	"""Must remove user from DB"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'DELETE FROM `usr` '
		f'WHERE uid = "{kwargs.get("user_id")}"')
	print(time.asctime() + f' User {kwargs.get("user_id")} removed from DB')


@dc.wishes_db_conn
def get_last_wish(gacha_id, **kwargs):
	"""Must return dict with user's last wish from table"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'SELECT MAX(id) '
		f'FROM `{gacha_id}` '
		f'WHERE uid="{kwargs.get("user_id")}"'
	)
	row = cursor.fetchone()
	if row["MAX(id)"]:
		return row["MAX(id)"]
	else:
		return None


@dc.wishes_db_conn
def append_wish(items, **kwargs) -> dict:
	"""Must append row with new item to DB"""
	dict_of_inserts = Counter()
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	for item in items:
		try:
			cursor.execute(
				f'INSERT INTO `{item.get("gacha_type")}` '
				f'VALUES ("{kwargs.get("user_id")}","{item["time"]}","{item["name"]}","{item["item_type"]}","{item["rank_type"]}","{item["id"]}");'
			)
			dict_of_inserts.update({item.get("gacha_type"): 1})
		except Exception as e:
			print(f'database.append_wish method: {e}')
			raise e
	return dict_of_inserts
