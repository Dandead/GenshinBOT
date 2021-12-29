from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from emoji import emojize
from src import exceptions, user


types_of_wishes = {
				"100": "Молитва новичка",
				"200": "Стандартная молитва",
				"301": "Молитва события персонажа",
				"400": "Молитва события персонажа II",
				"302": "Молитва события оружия"
			}

def register_handlers_wishes(dp: Dispatcher):
	dp.register_message_handler(get_link_from_user, filters.Text(equals=emojize("Ссылка :crystal_ball:")))
	dp.register_message_handler(enter_with_key, filters.Text(equals=emojize("Ключ :key:")))
	dp.register_message_handler(handling_link_from_user, state=Stages.waiting_for_link)
	dp.register_message_handler(waiting_for_options, state=Stages.waiting_for_option)
	dp.register_message_handler(choosing_type_of_data, state=Stages.choosing_type_of_data)


class Stages(StatesGroup):
	waiting_for_link = State()
	waiting_for_option = State()
	choosing_type_of_data = State()


async def enter_with_key(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer('В разработке...')
	return


async def get_link_from_user(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer('Пришлите ссылку на молитвы:', reply_markup=types.ReplyKeyboardRemove())
	await Stages.waiting_for_link.set()


async def handling_link_from_user(message: types.Message, state: FSMContext):
	try:
		new_genshin_user_copy = user.User(str(message))
		await state.update_data(genshin_user=new_genshin_user_copy)
		buttons = [
			emojize("Обновить список молитв :fireworks:"),
			emojize("Получить подробную статистику :bar_chart:"),
			emojize("Обновить/получить ключ :key:")
		]
		buttons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		buttons_keyboard.add(buttons[0]).row(*buttons[1:])
		await Stages.waiting_for_option.set()
		await message.answer("С чего начнем?", reply_markup=buttons_keyboard)
	except (exceptions.AuthKeyInvalidException, exceptions.AuthKeyMissedException, exceptions.DuplicateUserInLoop) as e:
		await message.answer(e.return_to_user())
		return
	except Exception as e:
		print(f'{type(e)} + {e}')
		await message.answer("Что-то пошло не так!\nСвяжитесь с разработчиком!")
		return


async def waiting_for_options(message: types.Message, state: FSMContext):
	if message.text == emojize("Обновить список молитв :fireworks:"):
		try:
			return_to_user = []
			await message.answer("Обрабатываем...")
			genshin_user = await state.get_data()
			genshin_user = genshin_user.get("genshin_user")
			updated_data: dict = await genshin_user.start_update_db()
			print(updated_data)
			for key, value in updated_data.items():
				return_to_user.append(f'<b><i><u>{types_of_wishes[key]}</u></i></b>: было добавлено {md.hcode(value)} новых молитв\n')
			await message.answer(''.join(return_to_user), parse_mode=types.ParseMode.HTML)
			return
		except Exception as e:
			print(e)
			raise e
	elif message.text == emojize("Получить подробную статистику :bar_chart:"):
		await message.answer("Учти, что на серверах игры хранятся данные о молитавах только за последние <u>6</u> месяцев", reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.HTML)
		buttons = [
			emojize("Узнать гарант :sparkles:"),
			emojize("Показать легендарки :star:")
		]
		buttons_keyboard = types.ReplyKeyboardMarkup().add(buttons[0]).add(buttons[1])
		await Stages.choosing_type_of_data.set()
		await message.answer("Пока я могу только это:", reply_markup=buttons_keyboard)
	elif message.text == emojize("Обновить/получить ключ :key:"):
		await message.answer("В разработке")
		return
	else:
		await message.answer("Выбери раздел с помощью клавиатуры:")
		return
	
	
async def choosing_type_of_data(message: types.Message, state: FSMContext):
	if message.text == emojize("Узнать гарант :sparkles:"):
		pass
	if message.text == emojize("Показать легендарки :star:"):
		pass
	else:
		await message.answer("Выбери раздел с помощью клавиатуры:")
		return
