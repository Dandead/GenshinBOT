import requests
import json


class Scrapper:
	def __init__(self, in_link, debug=False):
		self.in_link = in_link.strip().split('?')[1][:-5]  # cutting input link to get only the data
		with open('gacha_data.json') as f:  # init local data file
			self.gacha_data = json.load(f)
		if debug:  # return link + get() code
			self.debug()
		else:  # link gen + creating file + write data
			self.__write_gacha()
	
	def __link_gen(self, gacha=0, last_item=''):
		try:
			self.resp = requests.get(
				f'{self.gacha_data["begin_link"]}{self.in_link}&{self.gacha_data["gacha_type"][gacha]}&page=1&{self.gacha_data["size"]}&end_id={last_item}'
			)
			return self.resp
		except:
			return None
	
	def __user_file(self, json_obj=None, opened=False, fip=None):
		if opened is False:
			self.f = open(json_obj["data"]["list"][0]["uid"] + ".txt", "wt")
			return self.f
		else:
			fip.close()

	def __write_gacha(self):
		self.fp = self.__user_file(self.__link_gen().json())
		for x in range(0, 4):
			self.__item = ''
			while 1:
				self.__temp = self.__link_gen(x, self.__item).json()
				if len(self.__temp["data"]["list"]) == 0:
					break
				for i in range(0, len(self.__temp["data"]["list"])):
					self.fp.write(f'{self.__temp["data"]["list"][i]}\n')
				self.__item = self.__temp["data"]["list"][len(self.__temp["data"]["list"]) - 1]["id"]
		self.__user_file(None, True, self.fp)
	
	def debug(self):
		out = self.__link_gen()
		return print(out.url + '\nCode: ' + str(out.status_code))
	