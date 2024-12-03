from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_lobby = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать лобби для проведения опроса", callback_data="create_lobby"
            )
        ]
    ]
)
