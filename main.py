from wishes import *
from database_usage import *


link = str(input())
data = wish_data(link)[0]
authkey = wish_data(link, key_return=True)
user = check_user(**data)
if user:
	print("Ты есть в базе")
else:
	create_user(authkey=authkey, **data)
cursor = connect(**DATA).cursor(dictionary=True)
for gacha_type in GACHA_TYPES:
	end_id = ""
	while True:
		rn_data = wish_data(link, gacha_type, 20, end_id)
		if len(rn_data) != 0:
			for item in rn_data:
				# if check_wish() and not user:
				# 	break
				append_wish(cursor, **item)
			end_id = rn_data[len(rn_data)-1]["id"]
		else:
			break
close_db(cursor)
