import logging
import configparser
import mysql.connector
import aioredis
import src.exceptions as exceptions
from collections import Counter

logger = logging.getLogger(__name__)


def wishes_db_conn(func):
	"""Decorator for connection to "wishes" database"""
	def decorate(*args, **kwargs):
		try:
			pars = configparser.ConfigParser()
			pars.read("config/databases.ini")
			pars.read("/home/local/Documents/PyCharm/Tests/config/databases.ini")
			data = dict(pars.items('GENSHIN_USERS'))
			connect = mysql.connector.connect(**data)
			res = func(*args, conn=connect, **kwargs)
		except mysql.connector.Error as e:
			logger.critical(e)
			# raise e
		except exceptions.Error as e:
			logger.warning(e)
			raise e
		else:
			return res
		finally:
			connect.commit()
			connect.close()
	return decorate


@wishes_db_conn
def check_user(user_id: str, **kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM usr WHERE uid = "{user_id}"')
	row = cursor.fetchone()
	if row:
		return True
	else:
		return False


@wishes_db_conn
def create_user(user_id: str, **kwargs):
	"""Must append user's info string into DB."""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	if check_user(user_id):
		return
	cursor.execute(
		f'INSERT INTO `usr` '
		f'VALUES ("{user_id}","ru","{kwargs.get("authkey")}")')
	logger.info(f'User {user_id} created in DB')


@wishes_db_conn
def remove_user(**kwargs):
	"""Must remove user from DB"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	cursor.execute(
		f'DELETE FROM `usr` '
		f'WHERE uid = "{kwargs.get("user_id")}"')
	logger.info(f' User {kwargs.get("user_id")} removed from DB')


@wishes_db_conn
def get_last_wish(user_id: str, gacha_id: str, **kwargs):
	"""Must return dict with user's last wish from table"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	if gacha_id == "301":
		cursor.execute(
			f'SELECT MAX(id) '
			f'FROM `gacha_data` '
			f'WHERE (uid="{user_id}" and gacha_type="301") or (uid="{user_id}" and gacha_type="400")'
		)
	else:
		cursor.execute(
			f'SELECT MAX(id) '
			f'FROM `gacha_data` '
			f'WHERE uid="{user_id}" and gacha_type="{gacha_id}"'
	)
	row = cursor.fetchone()
	if row["MAX(id)"]:
		return row["MAX(id)"]
	else:
		return None


@wishes_db_conn
def append_wish(items, **kwargs) -> dict:
	"""Must append rows with new items to DB"""
	dict_of_inserts = Counter()
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	for item in items:
		try:
			cursor.execute(
				f'INSERT INTO `gacha_data` '
				f'VALUES ('
				f'"{item.get("uid")}", '
				f'"{item.get("gacha_type")}", '
				f'"{item.get("time")}", '
				f'"{item.get("name")}", '
				f'"{item.get("item_type")}", '
				f'"{item.get("rank_type")}", '
				f'"{item.get("id")}");'
			)
			dict_of_inserts.update({item.get("gacha_type"): 1})
		except Exception as e:
			raise e
	return dict_of_inserts


@wishes_db_conn
def get_legendary_items(user_id, **kwargs) -> dict:
	"""Return list of legendary items with banners id"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	try:
		to_return = {"100": [], "200": [], "301": [], "302": []}
		for gacha_id in ["100", "200", "301", "302"]:
			if gacha_id == "301":
				cursor.execute(
					f'SELECT res_tab.name, "301" as gacha_type, res_tab.rn as row_num, (res_tab.rn - lag(res_tab.rn) over()) AS garant '
					f'FROM ('
					f'	SELECT *, ROW_NUMBER() OVER(order by id) as rn'
					f'	FROM wishes.`gacha_data`'
					f'	WHERE (uid="{user_id}" and gacha_type="301") or (uid="{user_id}" and gacha_type="400")'
					f') AS res_tab '
					f'WHERE res_tab.rank_type=5 '
					f'ORDER BY res_tab.id'
				)
				data = cursor.fetchall()
				for item in data:
					to_return[str(item["gacha_type"])].append(item)
			else:
				cursor.execute(
					f'SELECT res_tab.name, res_tab.gacha_type, res_tab.rn as row_num, (res_tab.rn - lag(res_tab.rn) over()) AS garant '
					f'FROM ('
					f'	SELECT *, ROW_NUMBER() OVER(order by id) as rn'
					f'	FROM wishes.`gacha_data`'
					f'	WHERE uid="{user_id}" and gacha_type="{gacha_id}"'
					f') AS res_tab '
					f'WHERE res_tab.rank_type=5 '
					f'ORDER BY res_tab.id'
				)
				to_return.update({gacha_id: cursor.fetchall()})
		return to_return
	except Exception as e:
		raise e

	
@wishes_db_conn
def get_guarantee(user_id, **kwargs) -> dict:
	"""Return list of legendary items with banners id"""
	cursor = kwargs.pop("conn").cursor(dictionary=True)
	try:
		to_return = {}
		for gacha_id in ["100", "200", "301", "302"]:
			if gacha_id == "301":
				cursor.execute(
					f'SELECT res_tab.gacha_type, res_tab.rn-1 as row_num '
					f'FROM ( '
					f'	SELECT *, ROW_NUMBER() OVER(order by id DESC) as rn '
					f'	FROM wishes.`gacha_data` '
					f'	WHERE (uid="{user_id}" and gacha_type="301") or (uid="{user_id}" and gacha_type="400") '
					f'	ORDER BY id DESC '
					f'	LIMIT 90 '
					f') AS res_tab  '
					f'WHERE res_tab.rank_type=5 '
					f'ORDER BY id DESC '
					f'LIMIT 1'
				)
				data = cursor.fetchone()
				if data:
					to_return.update({"301": data.get("row_num")})
			else:
				cursor.execute(
					f'SELECT res_tab.gacha_type, res_tab.rn-1 as row_num '
					f'FROM ( '
					f'	SELECT *, ROW_NUMBER() OVER(order by id DESC) as rn '
					f'	FROM wishes.`gacha_data` '
					f'	WHERE uid="{user_id}" and gacha_type="{gacha_id}" '
					f'	ORDER BY id DESC '
					f'	LIMIT 90 '
					f') AS res_tab  '
					f'WHERE res_tab.rank_type=5 '
					f'ORDER BY id DESC '
					f'LIMIT 1'
				)
				data = cursor.fetchone()
				if data:
					to_return.update({gacha_id: data.get("row_num")})
		return to_return
	except Exception as e:
		raise e
	

async def duplicate_protection(uid: str, check: bool = False, remove: bool = False):
	config = configparser.ConfigParser()
	config.read("config/databases.ini")
	redis = await aioredis.from_url("redis://localhost", **dict(config.items("REDIS_DP")))
	try:
		if check:
			return bool(await redis.exists(uid))
		elif remove:
			await redis.delete(uid)
		else:
			await redis.set(uid, "")
	finally:
		await redis.close()

if __name__ == '__main__':
	print(create_user("715407122"))
