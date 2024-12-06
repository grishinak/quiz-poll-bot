from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# button to create_question fsm from /start command
drop_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Удалить все мои данные (опросы и вопросы)",
                callback_data="delete_user_data",
            )
        ],
    ]
)

check_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да, удалить все", callback_data="check_del_true"
            ),
            InlineKeyboardButton(
                text="Нет, отменить удаление", callback_data="check_del_false"
            ),
        ]
    ]
)
