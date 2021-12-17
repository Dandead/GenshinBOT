class AuthKeyMissedException(Exception):
	def __init__(self, *args):
		pass
	
	def __str__(self):
		return f'\033[31mAuthkey was missed. This link can\'t be processed\033[0m'


class AuthKeyInvalidException(Exception):
	def __init__(self, *args):
		self.message = args[0] if args else None
	
	def __str__(self):
		return f'\033[31mAuthkey was corrupted or invalid. ' \
			f'Returned error: {self.message}\033[0m'
