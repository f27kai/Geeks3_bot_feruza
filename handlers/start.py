import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import chat

from config import bot, ADMIN_ID, MEDIA_PATH
from database.a_db import AsyncDataBase
from database import sql_queries
from const import START_MENU_TEXT
from keyboards.start import start_menu_keyboard

router = Router()

@router.message(Command('start'))
async def start(message: types.Message, db=AsyncDataBase()):
    try:
        await db.execute_query(
            query=sql_queries.INSERT_USER_TABLE,
            params=(
                None,
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
            ),
            fetch = "None"
        )
    except sqlite3.IntegrityError:
        pass

    animation_file = types.FSInputFile(MEDIA_PATH + "bot-ani.gif")
    keyboard = start_menu_keyboard()
    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=animation_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await keyboard
    )



@router.message(lambda message: message.text == "feruza")
async def admin_feruza(message: types.Message, db=AsyncDataBase()):
    if int(ADMIN_ID) == message.from_user.id:
        users_data = await db.execute_query(query=sql_queries.READ_USER_TABLE, fetch="All")
        print(users_data)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Вы админ. Вот таблица из базы данных \n{users_data}")

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="К сожалению, вы не являетесь админом. Из-за этого мы не можем дать вам доступ"
        )



