import requests
from database_usage import *
import re
import logging

WISHES_LINK = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?"
KEY_VER = "authkey_ver=1"
GACHA_TYPES = ["100", "200", "301", "302"]
logging.basicConfig(
	filename='log/wishes.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)


def wish_data(link, wish="200", size="1", end="0", key_return=False, link_return=False) -> list:
	"""Returns link, JSON or authkey."""
	authkey = re.search(r'(?<=authkey=)[^&#]+', str(link), flags=re.MULTILINE).group()
	resp = f'{WISHES_LINK}{KEY_VER}&lang=ru&authkey={authkey}&gacha_type={wish}&size={size}&end_id={end}'
	message = requests.get(resp).json()["message"]
	if key_return:
		return [requests.get(resp).json()["data"]["list"], authkey]
	elif link_return:
		return [requests.get(resp).json()["data"]["list"], resp]
	elif not authkey or message != "OK":
		return None
	return requests.get(resp).json()["data"]["list"]


def check_user(cursor, **kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	cursor.execute(f'SELECT * FROM usr WHERE uid = "{kwargs["uid"]}"')
	row = cursor.fetchone()
	if row is not None:
		return True
	else:
		return False


def create_user(cursor, **w):
	"""Must append user's info string into DB."""
	lang = "en" if not w["lang"] else w["lang"][0:2]
	authkey = "NULL" if not w["authkey"] else w["authkey"]
	cursor.execute(
		f'INSERT INTO `usr` '
		f'VALUES ("{w["uid"]}","{lang}","{authkey}")')
	logging.info(f'User {w["uid"]} created in DB')


def remove_user(cursor, **w):
	"""Must remove user from DB"""
	cursor.execute(
		f'DELETE FROM usr '
		f'WHERE uid = "{w["uid"]}"')
	logging.info(f'User {w["uid"]} removed from DB')


def check_wish(cursor, **w) -> bool:
	"""Must return bool of existing user's item in DB."""
	cursor.execute(
		f'SELECT * '
		f'FROM `{w["gacha_id"]}` '
		f'WHERE id = "{w["id"]}";')
	row = cursor.fetchone()
	if row:
		return True
	else:
		return False


def get_last_wish(cursor, uid, gacha_id):
	"""Must return dict with user's last wish from table"""
	cursor.execute(
		f'SELECT id '
		f'FROM `{gacha_id}` '
		f'WHERE uid="{uid}" and id=('
		f'	SELECT MAX(id) '
		f'	FROM `{gacha_id}` '
		f'	WHERE time=('
		f'		SELECT MAX(time) '
		f'		FROM `{gacha_id}`'
		f'		)'
		f'	);'
	)
	row = cursor.fetchone()
	if row:
		return row["id"]
	else:
		return None


def append_wish(cursor, **item):
	"""Must append row with new item to DB"""
	cursor.execute(
		f'INSERT INTO `{item["gacha_id"]}` '
		f'VALUES ("{item["uid"]}","{item["time"]}","{item["name"]}","{item["item_type"]}","{item["rank_type"]}","{item["id"]}");'
	)


def start_wishes_update(link: str, gacha_id: str, uid: str, cursor):
	end_id = ""
	proc = True
	last_wish = get_last_wish(cursor, uid, gacha_id)
	count = 0
	while proc:
		item_list: list = wish_data(link, gacha_id, "20", end_id)
		if len(item_list) == 0:
			break
		for item in item_list:
			if item["id"] == last_wish:
				proc = False
				break
			append_wish(cursor, gacha_id=gacha_id, **item)
			count += 1
		end_id = item_list[len(item_list)-1]["id"]
	if count > 0:
		logging.info(f'Added {count} new rows to "{gacha_id}" table for "{uid}"')


@db_connect_decorator
def init(link, **kwargs):
	cursor = kwargs.pop('conn').cursor(dictionary=True)
	data, authkey = wish_data(link, key_return=True)
	if not check_user(cursor, **data[0]):
		create_user(cursor, authkey=authkey, **data[0])
	for gacha_id in GACHA_TYPES:
		start_wishes_update(link, gacha_id, data[0]["uid"], cursor)

