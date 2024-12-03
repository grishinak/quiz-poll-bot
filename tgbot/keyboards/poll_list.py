from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_lobby = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать лобби", callback_data="create_lobby")]
    ]
)
