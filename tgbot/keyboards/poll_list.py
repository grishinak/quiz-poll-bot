from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_lobby = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать опрос с моим вопросом", callback_data="create_lobby"
            )
        ]
    ]
)
