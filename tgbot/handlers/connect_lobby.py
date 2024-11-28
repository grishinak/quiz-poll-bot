from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Bot

import database.requests as rq

# import keyboards.connect_lobby as kb

router = Router()

# Обработчик команды /connect_lobby
@router.message(Command("connect_lobby"))
async def cmd_connect_lobby(message: Message, state: FSMContext, bot: Bot):
    # Проверим, если пользователь создатель лобби
    lobby_id = message.text.split()[1]  # Пример: /connect_lobby 1
    lobby_id = int(lobby_id)

    # Проверим существование лобби
    if not await rq.check_lobby_exists(lobby_id):
        await message.answer("Лобби не существует.")
        return

    # Добавляем пользователя в лобби
    if await rq.check_if_participant_exists(lobby_id, message.from_user.id):
        await message.answer("Вы уже в этом лобби!")
        return

    await rq.set_lobby_participant(lobby_id, message.from_user.id)
    await message.answer(f"Вы подключились к лобби {lobby_id}!")

    # Получим poll_id и сам вопрос
    poll_id = await rq.get_poll_id_for_lobby(lobby_id)
    question = await rq.get_poll_question(poll_id)

    # Получим всех участников лобби
    participants = await rq.get_lobby_participants(lobby_id)

    # Отправим вопрос всем участникам
    for participant_id in participants:
        # отправим вопрос каждому участнику лобби
        await bot.send_message(
            participant_id, f"Вопрос: {question}"
        )  # сейчас вопрос сразу при подключении к лобби отправлен
