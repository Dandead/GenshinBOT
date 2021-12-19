class AuthKeyMissedException(Exception):
	def __init__(self, *args):
		pass
	
	def __str__(self):
		return f'\033[31mAuthkey was missed. This link can\'t be processed\033[0m'


class AuthKeyInvalidException(Exception):
	def __init__(self, *args):
		self.message = args[0] if args else None
	
	def __str__(self):
		return f'\033[31mAuthkey is corrupted or invalid. ' \
			f'Returned error: {self.message}\033[0m'


class DuplicateUserInLoop(Exception):
	"""Called than copy of processing user tries to write data in DB"""
	def __init__(self, *args):
		pass
	
	def __str__(self):
		return f'\033[31mPlease, wait until this user is processed.'
