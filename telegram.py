from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import configparser
from emoji import emojize
import wishes

config = configparser.ConfigParser()
config.read('./config/bot.ini')

bot = Bot(**dict(config.items('telegram')))
dp = Dispatcher(bot)


class Stages(StatesGroup):
	waiting_for_link = State()
	waiting_for_choose_data = State()


@dp.message_handler(commands=['start', 'cancel'])
async def start(message: types.Message):
	start_buttons = [emojize("Ключ :key:"), emojize("Обновить молитвы :crystal_ball:")]
	buttons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	buttons_keyboard.add(*start_buttons)
	await message.answer('С чего начнем?', reply_markup=buttons_keyboard)


@dp.message_handler(filters.Text(equals=emojize("Ключ :key:")))
async def enter_with_key(message: types.Message):
	await message.answer('В разработке...')


@dp.message_handler(filters.Text(equals=emojize("Обновить молитвы :crystal_ball:")))
async def get_link_from_user(message: types.Message):
	await message.answer('Пришлите ссылку на молитвы:', reply_markup=types.ReplyKeyboardRemove())
	await Stages.waiting_for_link.set()


async def handling_link_from_user(message: types.Message, state: FSMContext):
	try:
		new_genshin_user_copy = wishes.User(message)
		asyncio.ensure_future(new_genshin_user_copy.start_update_db())
	except:
		pass


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
