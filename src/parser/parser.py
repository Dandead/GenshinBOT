import logging
import aiohttp
import requests
from src import exceptions


logger = logging.getLogger(__name__)


async def async_get_data(authkey: str, gacha_id: str, end_id: str) -> list:
	"""Must return lists of wishes data/only one list/link to json"""
	request_link_header = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1"
	request_link = f'{request_link_header}&lang=ru&authkey={authkey}&gacha_type={gacha_id}&size=20&end_id={end_id}'
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)).get(request_link) as resp:
		response = await resp.json()
	if response["message"] == "OK":
		return response["data"]["list"]
	else:
		raise exceptions.AuthKeyInvalidException(response["message"])
	
	
def get_uid(authkey: str):
	request_link_header = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1"
	for gacha_type in ["100", "200", "301", "302"]:
		request_link = f'{request_link_header}&lang=ru&authkey={authkey}&gacha_type={gacha_type}&size=1'
		response = requests.get(request_link).json()
		if response.get("message") == "OK":
			if response.get("data").get("list"):
				user_id = response.get("data").get("list")[0].get("uid")
				return user_id
		else:
			raise exceptions.AuthKeyInvalidException(response.get("message"))
	raise exceptions.UserWithoutWishes
