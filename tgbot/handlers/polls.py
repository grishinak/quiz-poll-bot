from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests as rq

import keyboards.polls as kb

router = Router()

# /question handler
@router.message(Command("polls"))
async def cmd_help(message: Message):
    await message.answer(
        "Что вы хотите сделать с опросами?", reply_markup=kb.polls_menu
    )


# Класс FSM для создания лобби
class CreatePoll(StatesGroup):
    polls = State()


@router.callback_query(F.data == "create_poll")
async def process_create_lobby_clb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали создание опроса!")
    await callback.message.answer("Вы начали создание опроса!")
    await state.set_state(CreatePoll.polls)
    await callback.message.answer(
        "Введите номер вопроса (после #), который вы хотите использовать для опроса:"
    )


@router.message(CreatePoll.polls)
async def process_poll_id(message: Message, state: FSMContext, bot: Bot):
    poll_id = message.text.strip()
    user_id = message.from_user.id

    try:
        polls = await rq.get_poll_by_id_and_creator(poll_id, user_id)
        if not polls:
            await message.answer(
                "Вопрос с таким ID не найден среди ваших вопросов. Попробуйте снова."
            )
            return

        lobby_id = await rq.set_poll(poll_id=int(poll_id), creator_id=user_id)

        await message.answer(
            f"Опрос #{lobby_id} успешно создан! Поделитесь этим номером с участниками. \n\nНе начинайте опрос пока они не подключатся.",
            reply_markup=kb.create_start_stop_poll_keyboard(lobby_id),
        )
    except Exception as e:
        await message.answer("Произошла ошибка при создании опроса. Попробуйте снова.")
        print(f"Ошибка при создании опроса: {e}")
    finally:
        await state.clear()


@router.callback_query(lambda call: call.data.startswith("start_poll"))
async def start_poll_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("Сбор ответов начат.")
    lobby_id = int(callback.data.split(":")[1])

    if not await rq.check_poll_exists(lobby_id):
        await callback.message.edit_text("Опроса не существует.")
        return

    # Установить флаг "сбор ответов" в True
    await rq.update_poll_collecting_status(lobby_id, True)

    poll_id = await rq.get_poll_id_for_lobby(lobby_id)
    question = await rq.get_poll_question(poll_id)
    participants = await rq.get_poll_participants(lobby_id)

    for participant_id in participants:
        await bot.send_message(
            participant_id, f"Вопрос: {question}", reply_markup=kb.give_answer
        )

    await callback.message.edit_text(
        "Опрос начат! Участники получили вопрос.",
        reply_markup=kb.create_stop_poll_keyboard(lobby_id),
    )


@router.callback_query(lambda call: call.data.startswith("stop_poll"))
async def stop_poll_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("Сбор ответов закончен.")
    lobby_id = int(callback.data.split(":")[1])

    # Установить флаг "сбор ответов" в False
    await rq.update_poll_collecting_status(lobby_id, False)

    participants = await rq.get_poll_participants(lobby_id)
    for participant_id in participants:
        await bot.send_message(
            participant_id,
            "Опрос завершен. Спасибо за участие!",
            reply_markup=kb.participants_end_menu,
        )

    await callback.message.edit_text("Опрос завершен!", reply_markup=kb.end_menu)


@router.callback_query(F.data == "polls_list")
async def show_polls_list_clb(callback: CallbackQuery):
    await callback.answer("Вы получаете список опросов.")

    user_id = callback.from_user.id  # ID пользователя Telegram

    # Получаем список опросов из базы данных
    polls = await rq.get_polls(user_id)

    # Если у пользователя нет созданных опросов
    if not polls:
        await callback.message.answer("У вас нет созданных опросов.")

    else:
        # Формируем сообщение со списком опросов
        response = "Ваши созданные опросы:\n\n"
        for lobby_id, poll_id, creator_id in polls:
            response += f" - Опрос #{lobby_id} с вопросом #{poll_id}\n"

        # Отправляем пользователю список опросов
        await callback.message.answer(response)


# FSM для подключения к опросу
class PollState(StatesGroup):
    waiting_for_poll_id = State()
    waiting_for_start_poll = State()
    answer = State()


# обработка нажатия кнопки from /start и переход в состояние
@router.callback_query(F.data == "connect_poll")
async def clb_connect_poll(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы подключаетесь к опросу.")
    await callback.message.answer("К какому опросу вы хотите подключиться?")
    await state.set_state(PollState.waiting_for_poll_id)


@router.message(PollState.waiting_for_poll_id)
async def process_poll_id(message: Message, state: FSMContext):
    try:
        lobby_id = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите действительный ID опроса.")
        return

    if not await rq.check_poll_exists(lobby_id):
        await message.answer("Опроса не существует.")
        return

    if await rq.check_if_participant_exists(lobby_id, message.from_user.id):
        await message.answer("Вы уже подключены к этому опросу!")
        return

    await rq.set_poll_participant(lobby_id, message.from_user.id)
    await state.update_data(lobby_id=message.text)
    await message.answer(f"Вы успешно подключились к опросу #{lobby_id}!")
    await state.set_state(PollState.waiting_for_start_poll)

    # await state.clear()


@router.message(PollState.waiting_for_start_poll)
async def process_answer(message: Message, state: FSMContext):
    await message.answer("Организатор еще не начал опрос, подождите.")


# Обработка нажатия кнопки (from start) и переход в состояние
@router.callback_query(F.data == "give_answer")
async def give_answer_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали отвечать на вопрос")  # alert

    await state.set_state(PollState.answer)  # goes to state
    await callback.message.answer("Введите ваш ответ: ")  # message in chat


@router.message(PollState.answer)
async def process_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()  # get all data about polls from user
    #     await message.answer(
    #         f"Все ли верно?\n\nОтвет: {data['answer']}",
    #         reply_markup=kb.check_menu,  # buttons for check
    #     )

    # # Обработка нажатия кнопки (from answer) и переход в состояние
    # @router.callback_query(F.data == "check_answer_false")
    # async def process_check_false(callback: CallbackQuery, state: FSMContext):
    #     await callback.message.edit_text("Данные не верны.")
    #     await callback.answer("Сначала")  # alert
    #     await callback.message.answer("Вы начали ввод ответа сначала!")  # message in chat

    #     await state.set_state(PollState.answer)  # goes to state
    #     await callback.message.answer("Введите ваш ответ: ")

    # # Обработка нажатия кнопки (from answer) и переход в состояние
    # @router.callback_query(F.data == "check_answer_true")
    # async def process_check_true(callback: CallbackQuery, state: FSMContext):
    #     await callback.answer("Успешно")  # alert
    #     await callback.message.edit_text("Данные верны.", reply_markup=None)
    data = await state.get_data()

    participant_id = message.from_user.id
    try:
        if await rq.is_poll_collecting(data["lobby_id"]):
            answer_id = await rq.set_answer(
                lobby_id=data["lobby_id"],
                participant_id=participant_id,
                user_answer=data["answer"],
            )

            # Отправляем сообщение пользователю о том, что опрос сохранен
            await message.answer(f"Ваш ответ '{data['answer']}' сохранен!")
        else:
            await message.answer(f"Время для ответа вышло. Опрос уже завершен.")

    except Exception as e:
        # Если произошла ошибка, информируем пользователя
        await message.answer(
            "Произошла ошибка при сохранении ответа. Попробуйте снова."
        )
        print(f"Ошибка при сохранении ответа: {e}")

    await state.clear()
