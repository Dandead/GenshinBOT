from emoji import emojize
from aiogram import types
from typing import Union


class Keyboards:
	@staticmethod
	def waiting_for_options_kb(button: int = None) -> Union[types.ReplyKeyboardMarkup, str]:
		buttons = [
			emojize("Обновить список молитв :fireworks:"),
			emojize("Получить статистику :bar_chart:"),
			emojize("Обновить/получить ключ :key:")
		]
		if button is not None:
			return buttons[button]
		buttons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		buttons_keyboard.add(buttons[0]).row(*buttons[1:])
		return buttons_keyboard
	
	@staticmethod
	def choosing_type_of_data_kb(button: int = None) -> Union[types.ReplyKeyboardMarkup, str]:
		buttons = [
			emojize("Узнать гарант :sparkles:"),
			emojize("Показать мои легендарки :star:"),
			emojize("Назад :hammer:")
		]
		if button is not None:
			return buttons[button]
		buttons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(*buttons[0:2]).add(
			buttons[2])
		return buttons_keyboard

