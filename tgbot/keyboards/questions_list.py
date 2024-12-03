from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_poll = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать опрос с моим вопросом", callback_data="create_poll"
            )
        ]
    ]
)
