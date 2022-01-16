import logging
import mysql.connector
import time
import configparser


logger = logging.getLogger("databases")


def wishes_db_conn(func):
	"""Decorator for connection to "wishes" database"""
	def decorate(*args, **kwargs):
		try:
			pars = configparser.ConfigParser()
			pars.read("config/databases.ini")
			data = dict(pars.items('GENSHIN_USERS'))
			connect = mysql.connector.connect(**data)
			res = func(*args, conn=connect, **kwargs)
		except mysql.connector.Error as e:
			logger.critical(e)
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
			logging.error(e)
			raise e
	return decorator


def async_errors_handler(func):
	"""Async errors handler"""
	async def decorator(*args, **kwargs):
		try:
			return await func(*args, **kwargs)
		except Exception as e:
			logging.error(e)
			raise e
	return decorator
