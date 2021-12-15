import mysql.connector
import time

GLOBAL_LOOP = []


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
				print(time.asctime()+" Please, wait until this user is processed.")
				return None
			# print(md5)
			GLOBAL_LOOP.append(md5)
			# print(GLOBAL_LOOP)
			result = func(md5, *args, **kwargs)
			return result
		except Exception as e:
			print(time.asctime()+' Error: '+str(e))
			GLOBAL_LOOP.pop(GLOBAL_LOOP.index(md5))
			# print(GLOBAL_LOOP)
			return None
	return decorator
