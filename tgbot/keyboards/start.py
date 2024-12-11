from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button to create_question fsm from /start command
start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать вопрос", callback_data="create_question")],
        [
            InlineKeyboardButton(
                text="Подключиться к опросу", callback_data="connect_poll"
            )
        ],
    ]
)
