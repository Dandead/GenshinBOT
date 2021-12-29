from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from emoji import emojize
from src import exceptions, user


def register_handlers_wishes(dp: Dispatcher):
	dp.register_message_handler(get_link_from_user, filters.Text(equals=emojize("Ссылка :crystal_ball:")))
	dp.register_message_handler(enter_with_key, filters.Text(equals=emojize("Ключ :key:")))
	dp.register_message_handler(handling_link_from_user, state=Stages.waiting_for_link)
	dp.register_message_handler(waiting_for_options, state=Stages.waiting_for_option)


class Stages(StatesGroup):
	waiting_for_link = State()
	waiting_for_option = State()


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
	# # print(new_genshin_user_copy)
	# if new_genshin_user_copy:
	# 	await new_genshin_user_copy.start_update_db()
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
			genshin_user = await state.get_data()
			genshin_user = genshin_user.get("gensin_user")
			genshin_user.start_update_db()
		except:
			pass
	return
