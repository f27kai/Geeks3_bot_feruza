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

@router.callback_query(lambda call: call.data == 'history')
async def detect_like_history_call(call: types.CallbackQuery, db=AsyncDataBase()):
    profiles = await db.execute_query(
        query=sql_queries.SELECT_LIKED_PROFILES,
        params=(
            call.from_user.id,
        ),
        fetch="All"
    )

    if profiles:
        randomizer = random.choice(profiles)

        random_profile = await db.execute_query(
            query=sql_queries.READ_PROFLE_TABLE,
            params=(
                randomizer['OWNER_TELEGRAM_ID'],
            ),
            fetch="One"
        )

        photo = types.FSInputFile(random_profile["PHOTO"])

        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname=random_profile['NICKNAME'],
                phone_number=random_profile['PHONE_NUMBER'],
                e_mail=random_profile['EMAIL'],
                bio=random_profile['BIO'],
            ),
            reply_markup=await history(tg_id=random_profile['TELEGRAM_ID'])
        )

    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Probably you haven't liked anyone."
        )