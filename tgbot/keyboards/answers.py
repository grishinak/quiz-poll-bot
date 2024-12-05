from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button to create_question fsm from /start command
answers_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Все ответы", callback_data="answers")],
        [InlineKeyboardButton(text="Ответы из последнего опроса", callback_data="ans")],
    ]
)
