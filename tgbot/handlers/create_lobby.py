from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests as rq

router = Router()

# Класс с состояниями FSM
class CreateLobby(StatesGroup):
    poll = State()


@router.message(Command("create_lobby"))
async def process_create_lobby_cmd(message: Message, state: FSMContext):
    """
    Начало процесса создания лобби. Перевод в состояние ожидания ввода ID опроса.
    """
    await message.answer("Вы начали создание лобби!")  # сообщение в чате
    await state.set_state(CreateLobby.poll)  # переходим в состояние
    await message.answer(
        "Введите номер опроса (после #), который вы хотите использовать для лобби:"
    )


@router.message(CreateLobby.poll)
async def process_poll_id(message: Message, state: FSMContext):
    """
    Обработка введенного ID опроса. Проверка существования и принадлежности опроса создателю.
    """
    poll_id = message.text.strip()
    user_id = message.from_user.id

    try:
        # Проверяем, существует ли опрос и принадлежит ли он пользователю
        poll = await rq.get_poll_by_id_and_creator(poll_id, user_id)
        if not poll:
            await message.answer(
                "Опрос с таким ID не найден среди ваших опросов. Попробуйте снова."
            )
            return

        # Сохраняем лобби в базе данных
        lobby_id = await rq.set_lobby(poll_id=int(poll_id), creator_id=user_id)

        # Уведомляем о создании лобби
        await message.answer(
            f"Лобби успешно создано! Сообщите участникам, чтобы они подключались к лобби #{lobby_id}."
        )
    except Exception as e:
        await message.answer("Произошла ошибка при создании лобби. Попробуйте снова.")
        print(f"Ошибка при создании лобби: {e}")
    finally:
        await state.clear()
