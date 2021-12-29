import asyncio
import time


# async def jopa(i: bool):
# 	if i:
# 		raise exceptions.AuthKeyInvalidException
# 	else:
# 		print('no errors')
#
#
# def popa(i: bool):
# 	if i:
# 		raise exceptions.DuplicateUserInLoop
# 	else:
# 		print('no errors1')
#
# async def main():
# 	e = str(input())
# 	if e == 'q':
# 		await jopa(True)
# 	elif e == 'w':
# 		await jopa(False)
# 	elif e == 'e':
# 		popa(True)
# 	# raise ValueError
# 	else:
# 		popa(False)

# o = wishes.User(str(input()))
# if o:
# 	await o.start_update_db()

def errors_handler(func):
	def decorator():
		try:
			i = func()
			return i
		except Exception as e:
			print(time.asctime() + ' Error: ' + str(e))
	return decorator


def async_errors_handler(func):
	async def decorator():
		try:
			i = await func()
			return i
		except Exception as e:
			print(time.asctime() + ' Error: ' + str(e))
			return decorator
	return decorator
	

@async_errors_handler
async def main():
	raise ValueError


@errors_handler
def main2():
	raise ValueError('12345')



if __name__ == '__main__':
	asyncio.run(main())
	# main2()
