from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать опрос", callback_data="create_poll")]
    ]
)


# menu_2 = ReplyKeyboardMarkup(
#     keyboard=[[KeyboardButton(text="reply")]],
#     resize_keyboard=True,
#     input_field_placeholder="Выберите пункт меню ...")
