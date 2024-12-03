from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button for check states in fsm create_poll
check_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да, сохранить мой ответ", callback_data="check_answer_true"
            ),
            InlineKeyboardButton(
                text="Нет, ввести еще раз", callback_data="check_answer_false"
            ),
        ]
    ]
)
