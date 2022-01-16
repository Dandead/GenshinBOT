class AuthKeyMissedException(Exception):
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'\033[31mAuthkey was missed. Link can\'t be processed. UID:{self.uid}\033[0m'
	
	def return_to_user(self):
		return "Не могу обработать, проверьте правильность ввода ссылки!"


class UserWithoutWishes(Exception):
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'\033[31mThat user can`t be processed without wishes. UID:{self.uid}\033[0m'
	
	def return_to_user(self):
		return "Прошло слишком много времени с последней молитвы либо их не было вовсе."


class AuthKeyInvalidException(Exception):
	def __init__(self, message: str = None, uid: str = None):
		self.message = message
		self.uid = uid
	
	def __str__(self):
		return f'\033[31mAuthkey is corrupted or invalid. Returned error: {self.message}. UID:{self.uid}\033[0m'
	
	def return_to_user(self):
		return f'Что-то пошло не так! Ошибка: {self.message}\nСвяжитесь с разработчиком, если не сможете решить проблему!'


class DuplicateUserInLoop(Exception):
	"""Called than copy of processing user tries to write data in DB"""
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'\033[Duplicate processing user. UID:{self.uid}.\033[0m'
	
	def return_to_user(self):
		return "Подождите, пока этот пользовательн будет обработан!"


class TryingToUpdateWithoutLink(Exception):
	"""Called than user tries to update db without in-game link"""
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'\033[31mUID:{self.uid} tries to update without link\033[0m'
	
	def return_to_user(self):
		return "Для обновления молитв введите ссылку на молитвы:"
