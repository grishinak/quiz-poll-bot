from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
