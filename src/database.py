import src.decorators as dc
from collections import Counter
import time


@dc.wishes_db_conn
def check_user(user_id: str, **kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM usr WHERE uid = "{user_id}"')
	row = cursor.fetchone()
	if row:
		return True
	else:
		return False


@dc.wishes_db_conn
def create_user(user_id: str, **kwargs):
	"""Must append user's info string into DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'INSERT INTO `usr` '
		f'VALUES ("{user_id}","en","{kwargs.get("authkey")}")')
	print(f'User {user_id} created in DB')


@dc.wishes_db_conn
def remove_user(**kwargs):
	"""Must remove user from DB"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'DELETE FROM `usr` '
		f'WHERE uid = "{kwargs.get("user_id")}"')
	print(time.asctime() + f' User {kwargs.get("user_id")} removed from DB')


@dc.wishes_db_conn
def get_last_wish(gacha_id, user_id, **kwargs):
	"""Must return dict with user's last wish from table"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'SELECT MAX(id) '
		f'FROM `{gacha_id}` '
		f'WHERE uid="{user_id}"'
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


@dc.wishes_db_conn
def get_legendary_items(user_id, gacha_id, **kwargs):
	"""Return list of legendary items with banners id"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	try:
		cursor.execute(
			f'SELECT res_tab.name, res_tab.rn as row_num, (res_tab.rn - lag(res_tab.rn) over()) AS garant '
			f'FROM ('
			f'	SELECT *, ROW_NUMBER() OVER(order by id) as rn'
			f'	FROM wishes.`{gacha_id}`'
			f'	WHERE uid="{user_id}"'
			f') AS res_tab '
			f'WHERE res_tab.rank_type=5 '
			f'ORDER BY id'
		)
		to_return = cursor.fetchall()
		return to_return
	except Exception as e:
		print(f'database.get_legendary_items method: {e}')
		raise e
	
	
def get_guarantee():
	pass


if __name__ == '__main__':
	# print(get_last_wish("301"))
	print(get_legendary_items('715407122', '301'))
	