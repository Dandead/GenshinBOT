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
			return res
		finally:
			connect.commit()
			connect.close()
	return decorate


# def close_db(connect):
# 	try:
# 		connect.close()
# 	except mysql.connector.Error as e:
# 		print(e)
# 		raise mysql.connector.Error


# def open_db():
# 	connect = mysql.connector.connect(**DATA)
# 	return connect.cursor(dictionary=True)
#
#
# if __name__ == "__main__":
# 	print(open_db())
	