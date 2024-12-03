from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_start_stop_lobby_keyboard(lobby_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления лобби (кнопки "Начать" и "Завершить").
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Начать", callback_data=f"start_poll:{lobby_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Завершить", callback_data=f"stop_poll:{lobby_id}"
                )
            ],
        ]
    )


def create_stop_lobby_keyboard(lobby_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления лобби (кнопку "Завершить").
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить", callback_data=f"stop_poll:{lobby_id}"
                )
            ]
        ]
    )


give_answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить на вопрос", callback_data="give_answer")]
    ]
)

end_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Получить список ответов", callback_data="show_answers"
            )
        ],
        [InlineKeyboardButton(text="Создать новый опрос", callback_data="create_poll")],
        [
            InlineKeyboardButton(
                text="Создать новое лобби с существующим опросом",
                callback_data="create_lobby",
            )
        ],
    ]
)
