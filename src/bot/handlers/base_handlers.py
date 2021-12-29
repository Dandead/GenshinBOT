from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from emoji import emojize


def register_handlers_base(dp: Dispatcher):
	dp.register_message_handler(cmd_start, commands=["start", "cancel"], state="*")


async def cmd_start(message: types.Message, state: FSMContext):
	await state.finish()
	start_buttons = [
		emojize("Ключ :key:"),
		emojize("Ссылка :crystal_ball:")
	]
	buttons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	buttons_keyboard.add(*start_buttons)
	await message.answer(
		'Привет!\nЯ бот для обработки молитв пользователей в игре Genshin Impact\nЕсли у тебя нет ключа, то входи по ссылке на молитвы!',
		reply_markup=buttons_keyboard)

