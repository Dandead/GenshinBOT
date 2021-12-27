import mysql.connector
import time
import hashlib
import configparser

GLOBAL_LOOP = []


def db_connect_decorator(func):
	"""Decorator for connection to MySQL database"""
	def decorate(*args, **kwargs):
		try:
			pars = configparser.ConfigParser()
			pars.read("./config/databases.ini")
			data = dict(pars.items('GENSHIN_USERS'))
			connect = mysql.connector.connect(**data)
			res = func(*args, conn=connect, **kwargs)
		except mysql.connector.Error as e:
			raise e
		else:
			return res
		finally:
			connect.commit()
			connect.close()
	return decorate


def errors_handler(func):
	"""Errors handler"""
	def decorator(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			return result
		except Exception as e:
			print(time.asctime()+' Error: '+str(e))
			return None
	return decorator
