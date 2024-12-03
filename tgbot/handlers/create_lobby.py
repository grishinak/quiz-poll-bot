from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests as rq

import keyboards.create_lobby as kb

router = Router()

# Класс FSM для создания лобби
class CreateLobby(StatesGroup):
    polls = State()


@router.message(Command("create_lobby"))
async def process_create_lobby_cmd(message: Message, state: FSMContext):
    await message.answer("Вы начали создание опроса!")
    await state.set_state(CreateLobby.polls)
    await message.answer(
        "Введите номер вопроса (после #), который вы хотите использовать для опроса:"
    )


@router.callback_query(F.data == "create_lobby")
async def process_create_lobby_clb(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали создание опроса!")
    await callback.message.answer("Вы начали создание опроса!")
    await state.set_state(CreateLobby.polls)
    await callback.message.answer(
        "Введите номер вопроса (после #), который вы хотите использовать для опроса:"
    )


@router.message(CreateLobby.polls)
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

        lobby_id = await rq.set_lobby(poll_id=int(poll_id), creator_id=user_id)

        await message.answer(
            f"Опрос #{lobby_id} успешно создан! Поделитесь этим номером с участниками. \n\nНе начинайте опрос пока они не подключатся.",
            reply_markup=kb.create_start_stop_lobby_keyboard(lobby_id),
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

    if not await rq.check_lobby_exists(lobby_id):
        await callback.message.edit_text("Опроса не существует.")
        return

    # Установить флаг "сбор ответов" в True
    await rq.update_lobby_collecting_status(lobby_id, True)

    poll_id = await rq.get_poll_id_for_lobby(lobby_id)
    question = await rq.get_poll_question(poll_id)
    participants = await rq.get_lobby_participants(lobby_id)

    for participant_id in participants:
        await bot.send_message(
            participant_id, f"Вопрос: {question}", reply_markup=kb.give_answer
        )

    await callback.message.edit_text(
        "Опрос начат! Участники получили вопрос.",
        reply_markup=kb.create_stop_lobby_keyboard(lobby_id),
    )


@router.callback_query(lambda call: call.data.startswith("stop_poll"))
async def stop_poll_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("Сбор ответов закончен.")
    lobby_id = int(callback.data.split(":")[1])

    # Установить флаг "сбор ответов" в False
    await rq.update_lobby_collecting_status(lobby_id, False)

    participants = await rq.get_lobby_participants(lobby_id)
    for participant_id in participants:
        await bot.send_message(
            participant_id,
            "Опрос завершен. Спасибо за участие!",
            reply_markup=kb.participants_end_menu,
        )

    await callback.message.edit_text("Опрос завершен!", reply_markup=kb.end_menu)
