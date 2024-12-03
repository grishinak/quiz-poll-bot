from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_start_stop_poll_keyboard(lobby_id: int) -> InlineKeyboardMarkup:
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


def create_stop_poll_keyboard(lobby_id: int) -> InlineKeyboardMarkup:
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
        [
            InlineKeyboardButton(
                text="Создать новый вопрос", callback_data="create_question"
            )
        ],
        [
            InlineKeyboardButton(
                text="Создать новый опрос",
                callback_data="create_poll",
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
                text="Подключиться к новому опросу", callback_data="connect_poll"
            )
        ],
        [
            InlineKeyboardButton(
                text="Создать свой вопрос", callback_data="create_question"
            )
        ],
    ]
)
