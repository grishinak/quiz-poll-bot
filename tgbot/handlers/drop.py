from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import keyboards.drop as kb
import database.requests as rq


router = Router()
start_text = """С помощью этого бота Вы можете проводить опросы.\n"""


@router.message(Command("drop"))
async def cmd_drop(message: Message):
    """drop command handler"""
    await rq.set_user(
        message.from_user.id, message.from_user.first_name, message.from_user.last_name
    )
    await message.answer(start_text, reply_markup=kb.drop_menu)


@router.callback_query(F.data == "delete_user_data")
async def process_create_lobby_clb(callback: CallbackQuery):
    await callback.message.edit_text(
        "Вы действительно хотите сбросить свои вопросы и опросы?",
        reply_markup=kb.check_menu,
    )


@router.callback_query(F.data == "check_del_false")
async def process_check_false(callback: CallbackQuery):
    await callback.message.edit_text("Отмена удаления вопросов и опросов.")


@router.callback_query(F.data == "check_del_true")
async def process_check_true(callback: CallbackQuery):
    await callback.answer("Удаление списка вопросов и опросов")  # alert
    await callback.message.edit_text("Удаление списка вопросов и опросов.")
    await rq.delete_user_polls_and_questions(callback.from_user.id)
    await callback.message.edit_text("Данные удалены")
