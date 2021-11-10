import mysql.connector


DATA = {
	"host": "localhost",
	"database": "wishes",
	"user": "genshin",
	"password": "genshinpass"
}


def db_connect_decorator(func, **data):
	"""Decorator for connection to MySQL database"""
	def decorate(*args, **kwargs):
		try:
			connect = mysql.connector.connect(**DATA)
			res = func(*args, conn=connect, **kwargs)
			return res
		except mysql.connector.Error as e:
			print(e)
		else:
			connect.commit()
		finally:
			connect.close()
	return decorate

