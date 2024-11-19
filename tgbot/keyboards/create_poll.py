from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

check_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, все верно", callback_data="check_true"),
            InlineKeyboardButton(
                text="Нет, создать заново", callback_data="check_false"
            ),
        ]
    ]
)

# save_menu = ReplyKeyboardMarkup(
#     keyboard=[[KeyboardButton(text="Сохранить опрос.")]],
#     resize_keyboard=True,
#     input_field_placeholder="Нажмите на кнопку ...",
#     one_time_keyboard=True,
# )
