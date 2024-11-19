from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button to create_poll fsm from /start command
start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать опрос", callback_data="create_poll")]
    ]
)
