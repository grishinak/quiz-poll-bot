from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_start_stop_lobby_keyboard(lobby_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления лобби (кнопки "Начать" и "Завершить").
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Начать опрос. (Отправить вопрос участникам)",
                    callback_data=f"start_poll:{lobby_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Завершить опрос. (Прекратить сбор ответов)",
                    callback_data=f"stop_poll:{lobby_id}",
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
                    text="Завершить опрос. (Прекратить сбор ответов)",
                    callback_data=f"stop_poll:{lobby_id}",
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
                text="Создать новое лобби",
                callback_data="create_lobby",
            )
        ],
    ]
)

participants_end_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        # TODO: we may send participants results?
        #     [
        #         InlineKeyboardButton(
        #             text="Получить список ответов", callback_data="show_answers"
        #         )
        #     ],
        [
            InlineKeyboardButton(
                text="Подключиться к новому лобби", callback_data="connect_lobby"
            )
        ],
        [InlineKeyboardButton(text="Создать свой опрос", callback_data="create_poll")],
    ]
)
