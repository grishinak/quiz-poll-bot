from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

questions_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать вопрос", callback_data="create_question"
            ),
            InlineKeyboardButton(
                text="Список вопросов", callback_data="questions_list"
            ),
        ]
    ]
)


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

create_poll = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать опрос с моим вопросом", callback_data="create_poll"
            )
        ]
    ]
)
