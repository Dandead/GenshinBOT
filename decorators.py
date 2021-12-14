import mysql.connector
from main import GLOBAL_LOOP


DATA = {
	"host": "localhost",
	"database": "wishes",
	"user": "genshin",
	"password": "genshinpass"
}


def db_connect_decorator(func):
	"""Decorator for connection to MySQL database"""
	def decorate(*args, **kwargs):
		try:
			connect = mysql.connector.connect(**DATA)
			res = func(*args, conn=connect, **kwargs)
		except mysql.connector.Error as e:
			print(e)
		else:
			return res
		finally:
			connect.commit()
			connect.close()
	return decorate


def duplicates_protection(func):
	"""Decorator, that should protect event loop from duplicates"""
	def decorator(md5, *args, **kwargs):
		try:
			if md5 in GLOBAL_LOOP:
				return "Please, wait until this user is processed."
			print(md5)
			GLOBAL_LOOP.append(md5)
			result = func(*args, **kwargs)
			return result
		except:
			raise ValueError
		finally:
			GLOBAL_LOOP.pop(md5)
	return decorator
