import random
import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import chat, CallbackQuery, FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from database.a_db import AsyncDataBase
from database import sql_queries
from const import PROFILE_TEXT
from database.sql_queries import READ_ALL_PROFILES
from keyboards.like_dislike import history
from keyboards.start import start_menu_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

@router.callback_query(lambda call: call.data == 'WalletId')
async def wallet_id_users(call: types.CallbackQuery, db=AsyncDataBase()):
    wallet_users = await db.execute_query(
            query=sql_queries.READ_ALL_USER_TABLE_QUELY,
            fetch="All"
        )
    if wallet_users:
        other_wallets = [(wallet['ID'], wallet['FIRST_NAME'])  for wallet in wallet_users if wallet['TELEGRAM_ID'] != call.from_user.id]

        if other_wallets:
            wallet_ids_string = '\n'.join(str(wallet_id) for wallet_id in other_wallets)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"All wallet IDs, except yours:\n"
                     f"{wallet_ids_string}",
            )

        else:
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"No other wallet IDs found, except yours.",
            )

    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="No wallet IDs found."
        )

