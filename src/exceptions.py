class Error(Exception):
	"""Base class for all exceptions"""
	pass


class AuthKeyMissedException(Error):
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'Authkey was missed. Link can\'t be processed. UID:{self.uid}'
	
	def return_to_user(self):
		return "Не могу обработать, проверьте правильность ввода ссылки!"


class UserWithoutWishes(Error):
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'That user can`t be processed without wishes. UID:{self.uid}'
	
	def return_to_user(self):
		return "Прошло слишком много времени с последней молитвы либо их не было вовсе."


class AuthKeyInvalidException(Error):
	def __init__(self, message: str = None, uid: str = None):
		self.message = message
		self.uid = uid
	
	def __str__(self):
		return f'Authkey is corrupted or invalid. Returned error: {self.message}. UID:{self.uid}'
	
	def return_to_user(self):
		return f'Что-то пошло не так! Ошибка: {self.message}\nСвяжитесь с разработчиком, если не сможете решить проблему!'


class DuplicateUserInLoop(Error):
	"""Called than copy of processing user tries to write data in DB"""
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'Duplicate processing user. UID:{self.uid}.'
	
	def return_to_user(self):
		return "Подождите, пока этот пользовательн будет обработан!"


class TryingToUpdateWithoutLink(Error):
	"""Called than user tries to update db without in-game link"""
	def __init__(self, uid: str = None):
		self.uid = uid
	
	def __str__(self):
		return f'UID:{self.uid} tries to update without link	'
	
	def return_to_user(self):
		return "Для обновления молитв введите ссылку на молитвы:"
