from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Создать опрос")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню ...",
)
