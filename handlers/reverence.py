import binascii
import os
import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import chat, CallbackQuery, FSInputFile
from aiogram.utils.deep_linking import create_start_link

from config import bot, ADMIN_ID, MEDIA_PATH
from database.a_db import AsyncDataBase
from database import sql_queries
from const import PROFILE_TEXT
from database.sql_queries import READ_PROFLE_TABLE
from keyboards.reverence import reverence_menu_keyboards
from keyboards.start import start_menu_keyboard

router = Router()

@router.callback_query(lambda call: call.data == "reverence_menu")
async def reverence_menu(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text = "Hi, This is Reverence Menu!\n"
               "You can create Reverence link, share with your friends\n"
               "We will send to your account wallet 100 points",

        reply_markup = await reverence_menu_keyboards()
    )


@router.callback_query(lambda call: call.data == "reverence_link")
async def reverence_link_creation(call: types.CallbackQuery, db=AsyncDataBase()):
    token = binascii.hexlify(os.urandom(8)).decode()
    link = await create_start_link(bot=bot, payload=token)
    print(link)
    user = await db.execute_query(
        query=sql_queries.READ_ALL_USER_TABLE,
        params=(
            call.from_user.id,
        ),
        fetch="One"
    )
    print(user)

    print(user["REVERENCE_LINK"])

    if user["REVERENCE_LINK"]:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваш линк: {user['REVERENCE_LINK']}"
        )
    else:
        await db.execute_query(
                query=sql_queries.UPDATE_REVERENCE_USER_LINK,
                params=(
                    link,
                    call.from_user.id,
                ),
                fetch="None"
            )

        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваш линк: {link}"
        )


@router.callback_query(lambda call: call.data == "reverence_balance")
async def view_balance(call: types.CallbackQuery, db=AsyncDataBase()):
    user = await db.execute_query(
        query=sql_queries.READ_ALL_USER_TABLE,
        params=(
            call.from_user.id,
        ),
        fetch="One"
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text = f"Ваш баланс {user['BALANCE']}"
    )


@router.callback_query(lambda call: call.data == "reverence_list")
async def reverence_list(call: types.CallbackQuery, db=AsyncDataBase()):
    user = await db.execute_query(
        query=sql_queries.READ_REVERENCE_USER,
        params=(
            call.from_user.id,
        ),
        fetch="All"
    )

    print(user)
    if user:
        reverence_user = [ref['REVERENCE_TELEGRAM_ID'] for ref in user]
        await bot.send_message(
            chat_id=call.from_user.id,
            text = f"Список ваших референсов (ID)\n"
                   f"{reverence_user}"
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text = "К сожалению, вы не привели ни одного реферала."
        )