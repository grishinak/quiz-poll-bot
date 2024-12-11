from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

answers_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Все ответы", callback_data="answers")],
        [InlineKeyboardButton(text="Ответы из последнего опроса", callback_data="ans")],
    ]
)
