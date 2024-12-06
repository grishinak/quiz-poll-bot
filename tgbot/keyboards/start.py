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
