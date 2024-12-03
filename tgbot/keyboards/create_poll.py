from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button for check states in fsm create_question
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


questions_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои вопросы", callback_data="questions_list")]
    ]
)
