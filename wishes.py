import requests
from decorators import *
import re

WISHES_LINK = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?"
KEY_VER = "authkey_ver=1"





# def language(link, usr_lang=None) -> str:
# 	"""Returns user default lang with second arg, or lang from link."""
# 	lang = re.search(r'(?<=lang=)[^&#]+', str(link), flags=re.MULTILINE).group()
# 	if usr_lang:
# 		return usr_lang
# 	elif lang is None:
# 		return "en"
# 	else:
# 		return lang


def wish_data(link, wish=200, size=1, end=0, key_return=False, link_return=False):
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
	return requests.get(resp).json()


@db_connect_decorator
def check_user(**kwargs) -> bool:
	"""Must return bool of existing user in DB."""
	connect = kwargs.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM wishes.usr WHERE uid = "{kwargs["uid"]}"')
	row = cursor.fetchone()
	if row is not None:
		return True
	else:
		return False


@db_connect_decorator
def create_user(**w):
	"""Must return bool of existing user in DB."""
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'INSERT INTO wishes.usr VALUES ("{w["uid"]}", "{w["lang"]}", "{w["authkey"]}")')


@db_connect_decorator
def check_wish(**w) -> bool:
	"""Must return bool of existing user's item in DB."""
	connect = w.pop("conn")
	cursor = connect.cursor(dictionary=True)
	cursor.execute(f'SELECT * FROM wishes.{w["gacha_type"]} WHERE id = "{w["id"]}"')
	row = cursor.fetchone()
	if row is not None:
		return True
	else:
		return False


@db_connect_decorator
def write_wish(**w):				# without decorator because function will be called often
	"""Must append row with new item to DB"""
	pass
