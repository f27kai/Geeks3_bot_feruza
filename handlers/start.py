from aiogram import Router, types
from aiogram.filters import Command

from config import bot

router = Router()

@router.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}"
    )
