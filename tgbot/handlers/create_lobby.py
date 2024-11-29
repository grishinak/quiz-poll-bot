from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests as rq

import keyboards.create_lobby as kb

router = Router()

# Класс FSM для создания лобби
class CreateLobby(StatesGroup):
    poll = State()


@router.message(Command("create_lobby"))
async def process_create_lobby_cmd(message: Message, state: FSMContext):
    await message.answer("Вы начали создание лобби!")
    await state.set_state(CreateLobby.poll)
    await message.answer(
        "Введите номер опроса (после #), который вы хотите использовать для лобби:"
    )


@router.message(CreateLobby.poll)
async def process_poll_id(message: Message, state: FSMContext, bot: Bot):
    poll_id = message.text.strip()
    user_id = message.from_user.id

    try:
        poll = await rq.get_poll_by_id_and_creator(poll_id, user_id)
        if not poll:
            await message.answer(
                "Опрос с таким ID не найден среди ваших опросов. Попробуйте снова."
            )
            return

        lobby_id = await rq.set_lobby(poll_id=int(poll_id), creator_id=user_id)

        await message.answer(
            f"Лобби #{lobby_id} успешно создано! Поделитесь этим номером с участниками.",
            reply_markup=kb.create_start_stop_lobby_keyboard(lobby_id),
        )
    except Exception as e:
        await message.answer("Произошла ошибка при создании лобби. Попробуйте снова.")
        print(f"Ошибка при создании лобби: {e}")
    finally:
        await state.clear()


@router.callback_query(lambda call: call.data.startswith("start_poll"))
async def start_poll_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("Сбор ответов начат.")
    lobby_id = int(callback.data.split(":")[1])

    if not await rq.check_lobby_exists(lobby_id):
        await callback.message.edit_text("Лобби не существует.")
        return

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
    participants = await rq.get_lobby_participants(lobby_id)
    # TODO: logic when its over (deleting?)
    for participant_id in participants:
        await bot.send_message(participant_id, "Опрос завершен. Спасибо за участие!")

    await callback.message.edit_text("Опрос завершен!")
