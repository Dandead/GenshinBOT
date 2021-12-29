class AuthKeyMissedException(Exception):
	def __init__(self, *args):
		pass
	
	def __str__(self):
		return f'\033[31mAuthkey was missed. This link can\'t be processed\033[0m'
	
	def return_to_user(self):
		return "Не могу обработать, проверьте правильность ввода ссылки!"


class AuthKeyInvalidException(Exception):
	def __init__(self, message):
		self.message = message if message else None
	
	def __str__(self):
		return f'\033[31mAuthkey is corrupted or invalid. ' \
			f'Returned error: {self.message}\033[0m'
	
	def return_to_user(self):
		return f'Что-то пошло не так! Ошибка: {self.message}\nСвяжитесь с разработчиком, если не сможете решить проблему!'


class DuplicateUserInLoop(Exception):
	"""Called than copy of processing user tries to write data in DB"""
	def __init__(self, *args):
		pass
	
	def __str__(self):
		return f'\033[31mPlease, wait until this user is processed.\033[0m'
	
	def return_to_user(self):
		return "Подождите, пока этот пользовательн будет обработан!"
