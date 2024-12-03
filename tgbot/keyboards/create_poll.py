from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button for check states in fsm create_poll
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


poll_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Посмотреть список созданных опросов", callback_data="poll_list"
            )
        ]
    ]
)
