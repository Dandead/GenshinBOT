import aiohttp.client
from src import exceptions

request_link_header = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1"


async def get_data(authkey: str, gacha_id: str, end_id: str, link_return: bool = None):
	"""Must return lists of wishes data/only one list/link to json"""
	request_link = f'{request_link_header}&lang=en&authkey={authkey}&gacha_type={gacha_id}&size=20&end_id={end_id}'
	if link_return:
		return request_link
	async with aiohttp.ClientSession().get(request_link) as resp:
		response = await resp.json()
	if response["message"] == "OK":
		return response["data"]["list"]
	else:
		raise exceptions.AuthKeyInvalidException(response["message"])