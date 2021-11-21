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


def wish_data(link, wish="200", size="1", end="0", key_return=False, link_return=False):
	"""Returns link, JSON or authkey."""
	authkey = re.search(r'(?<=authkey=)[^&#]+', str(link), flags=re.MULTILINE).group()
	resp = f'{WISHES_LINK}{KEY_VER}&lang=ru&authkey={authkey}&gacha_type={wish}&size={size}&end_id={end}'
	message = requests.get(resp).json()["message"]
	if key_return:
		return authkey
	elif link_return:
		return resp
	elif not authkey or message != "OK":
		return None
	return requests.get(resp).json()["data"]["list"]


@db_connect_decorator
def check_user(**kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	connect = kwargs.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM usr WHERE uid = "{kwargs["uid"]}"')
	row = cursor.fetchone()
	if row is not None:
		return True
	else:
		return False


@db_connect_decorator
def create_user(**w):
	"""Must append user's info string into DB."""
	lang = "en" if not w["lang"] else w["lang"][0:2]
	authkey = "NULL" if not w["authkey"] else w["authkey"]
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'INSERT INTO usr VALUES ("{w["uid"]}", "{lang}", "{authkey})"')
	logging.info(f'User {w["uid"]} created in DB')


@db_connect_decorator
def remove_user(**w):
	"""Must remove user from DB"""
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'DELETE FROM usr WHERE uid = "{w["uid"]}"')
	logging.info(f'User {w["uid"]} removed from DB')


@db_connect_decorator
def check_wish(**w) -> bool:
	"""Must return bool of existing user's item in DB."""
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM {w["gacha_type"]} WHERE id = "{w["id"]}"')
	row = cursor.fetchone()
	if row:
		return True
	else:
		return False


@db_connect_decorator
def append_wish(**w):
	"""Must append row with new item to DB"""
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	print(cursor)
	cursor.execute(
		f'INSERT INTO `{w["gacha_type"]}` VALUES ("{w["uid"]}","{w["time"]}","{w["name"]}","{w["item_type"]}","{w["rank_type"]}","{w["id"]}");'
	)
	
	
# def start_update(link):
# 	data, authkey = wish_data(link), wish_data(link, key_return=True)
# 	if check_user(**data[0]):
# 		user_exist = True
# 	else:
# 		create_user(**data[0])
# 		user_exist = False
# 	cursor = connect(**DATA).cursor(dictionary=True)
# 	for gacha_type in GACHA_TYPES:
# 		end_id = ""
# 		while True:
# 			rn_data = wish_data(link, gacha_type, 20, end_id)
# 			if len(rn_data) != 0:
# 				for item in rn_data:
# 					# if check_wish() and not user:
# 					# 	break
# 					append_wish(cursor, **item)
# 				end_id = rn_data[len(rn_data) - 1]["id"]
# 			else:
# 				break
# 	close_db(cursor)

if __name__ == "__main__":
	append_wish(open_db(), **wish_data(str(input()))[0])