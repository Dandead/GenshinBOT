import logging

from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from src import database as db, exceptions, user
from src.bot import keyboards as kb
from emoji import emojize
import re


logger = logging.getLogger("bot")
types_of_wishes = {
				"100": "Молитва новичка",
				"200": "Стандартная молитва",
				"301": "Молитва события персонажа",
				"400": "Молитва события персонажа II",
				"302": "Молитва события оружия"			}


def register_handlers_wishes(dp: Dispatcher):
	dp.register_message_handler(get_link_from_user, filters.Text(equals=emojize("Ссылка :crystal_ball:")))
	dp.register_message_handler(get_key_from_user, filters.Text(equals=emojize("Ключ :key:")))
	dp.register_message_handler(handling_key_from_user, state=Stages.waiting_for_key)
	dp.register_message_handler(handling_link_from_user, state=Stages.waiting_for_link)
	dp.register_message_handler(waiting_for_options, state=Stages.waiting_for_option)
	dp.register_message_handler(choosing_type_of_data, state=Stages.choosing_type_of_data)


class Stages(StatesGroup):
	waiting_for_link = State()
	waiting_for_key = State()
	waiting_for_option = State()
	choosing_type_of_data = State()


async def get_key_from_user(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer('Введи свой ключ:\nДля возврата назад /cancel', reply_markup=types.ReplyKeyboardRemove())
	await Stages.waiting_for_key.set()


async def get_link_from_user(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer('Пришлите ссылку на молитвы:\nДля возврата назад /cancel', reply_markup=types.ReplyKeyboardRemove())
	await Stages.waiting_for_link.set()
	

async def handling_key_from_user(message: types.Message, state: FSMContext):
	key = re.fullmatch(r'[0-9]{9}', message.text)
	if key:
		key = key.group()
		if db.check_user(key):
			await state.update_data(genshin_user=key)
			await message.answer("С чего начнем?", reply_markup=kb.Keyboards.waiting_for_options_kb())
			await Stages.waiting_for_option.set()
		else:
			await message.answer("Неверный ключ!")
			return
	else:
		await message.answer("Неверный ключ!")
		return


async def handling_link_from_user(message: types.Message, state: FSMContext):
	try:
		new_genshin_user = user.User(link=str(message))
		await state.update_data(genshin_user=new_genshin_user.user_id, authkey=new_genshin_user.authkey)
		await message.answer(f'С чего начнем?', reply_markup=kb.Keyboards.waiting_for_options_kb())
		await Stages.waiting_for_option.set()
	except (exceptions.AuthKeyInvalidException, exceptions.AuthKeyMissedException) as e:
		await message.answer(e.return_to_user())
		logger.warning(message.chat.id)
		return
	except Exception as e:
		logger.error(e)
		await message.answer("Что-то пошло не так!\nСвяжитесь с разработчиком!")
		return


async def waiting_for_options(message: types.Message, state: FSMContext):
	if message.text == kb.Keyboards.waiting_for_options_kb(0): 	# update db with new wishes
		try:
			return_to_user = []
			await message.answer("Обрабатываем...")
			state_data = await state.get_data()
			genshin_user = state_data.get("genshin_user")
			authkey = state_data.get("authkey")
			if not authkey:
				await message.answer("Для обновления молитв зайдите, используя ссылку!\nДля возврата вначало /cancel")
				return
			instance = user.User(uid=genshin_user, authkey=authkey)
			updated_data: dict = await instance.start_update_db()
			for key, value in updated_data.items():
				return_to_user.append(f'<b><i><u>{types_of_wishes[key]}</u></i></b>: было добавлено {md.hcode(value)} новых молитв\n')
			await message.answer(''.join(return_to_user), parse_mode=types.ParseMode.HTML)
			return
		except exceptions.DuplicateUserInLoop as e:
			await message.answer("Пожалуйста, подождите пока этот пользователь будет обработан!")
			logger.warning("Duplicate user in writing loop", extra={"user": "message.chat.id"})
		except Exception as e:
			logger.error(e, extra={"user": "message.chat.id"})
			await message.answer("Что-то пошло не так!\nСвяжитесь с разработчиком!")
	elif message.text == kb.Keyboards.waiting_for_options_kb(1):
		await message.answer("Учти, что на серверах игры хранятся данные о молитавах только за последние <u>6</u> месяцев", parse_mode=types.ParseMode.HTML)
		await Stages.choosing_type_of_data.set()
		await message.answer("Пока я могу только это:", reply_markup=kb.Keyboards.choosing_type_of_data_kb())
	elif message.text == kb.Keyboards.waiting_for_options_kb(2):
		state_data = await state.get_data()
		user_id = state_data.get("genshin_user")
		await message.answer(f'Твой ключ для входа без ссылки: {md.hcode(user_id)}\n', parse_mode=types.ParseMode.HTML)
		return
	else:
		await message.answer("Выбери раздел с помощью клавиатуры:", reply_markup=kb.Keyboards.waiting_for_options_kb())
		return
	
	
async def choosing_type_of_data(message: types.Message, state: FSMContext):
	if message.text == kb.Keyboards.choosing_type_of_data_kb(0):		# Garant
		await message.answer('В разработке...')
		return
	elif message.text == kb.Keyboards.choosing_type_of_data_kb(1):		# all legendary items
		state_data = await state.get_data()
		genshin_user = state_data.get("genshin_user")
		return_to_user = {}
		response = []
		for key, value in types_of_wishes.items():
			temp = db.get_legendary_items(genshin_user, key)
			if temp:
				return_to_user[key] = temp
			else:
				pass
		if return_to_user:
			for key, value in return_to_user.items():
				response.append(f'<b><i><u>{types_of_wishes[key]}</u></i></b>:')
				for item in value:
					if item.get("garant") is None:
						response.append(f'<b>{item.get("name")}</b> - на <u>{item.get("row_num")}</u> крутке')
					else:
						response.append(f'<b>{item.get("name")}</b> - на <u>{item.get("garant")}</u> крутке')
			await message.answer("\n".join(response), parse_mode=types.ParseMode.HTML)
		else:
			await message.answer("На данный момент у тебя нет легендарок")
	elif message.text == kb.Keyboards.choosing_type_of_data_kb(2):
		await message.answer("С чего начнем?", reply_markup=kb.Keyboards.waiting_for_options_kb())
		await Stages.waiting_for_option.set()
	else:
		await message.answer("Выбери раздел с помощью клавиатуры:", reply_markup=kb.Keyboards.choosing_type_of_data_kb())
		return
