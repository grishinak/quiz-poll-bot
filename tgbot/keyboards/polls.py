from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


polls_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Создать опрос", callback_data="create_poll")],
        [
            InlineKeyboardButton(text="Ваши опросы", callback_data="polls_list"),
            # Была скрыта, к ней и так есть доступ через \questions
            # InlineKeyboardButton(text="Ваши вопросы", callback_data="questions_list"), # hided from interface
        ],
        [
            InlineKeyboardButton(
                text="Подключиться к опросу", callback_data="connect_poll"
            )
        ],
    ]
)


def create_start_stop_poll_keyboard(poll_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления лобби (кнопки "Начать" и "Завершить").
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Начать опрос. (Отправить вопрос участникам)",
                    callback_data=f"start_poll:{poll_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Завершить опрос. (Прекратить сбор ответов)",
                    callback_data=f"stop_poll:{poll_id}",
                )
            ],
        ]
    )


def create_stop_poll_keyboard(poll_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления лобби (кнопку "Завершить").
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить опрос. (Прекратить сбор ответов)",
                    callback_data=f"stop_poll:{poll_id}",
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
                text="Список ответов в последнем опросе", callback_data="ans"
            )
        ],
        [
            InlineKeyboardButton(
                text="Получить список ответов со всех опросов", callback_data="answers"
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
        [
            InlineKeyboardButton(
                text="Получить список опросов", callback_data="polls_list"
            )
        ],
    ]
)

participants_end_menu = InlineKeyboardMarkup(
    inline_keyboard=[
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
