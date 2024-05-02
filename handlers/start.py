import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command

from config import bot, ADMIN_ID
from database.a_db import AsyncDataBase
from database import sql_queries

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

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello {message.from_user.first_name}"
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



