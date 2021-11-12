import mysql.connector


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
			connect.commit()
		finally:
			connect.close()
		return res
	return decorate


def close_db(connect):
	try:
		connect.close()
	except mysql.connector.Error as e:
		print(e)
		raise mysql.connector.Error
