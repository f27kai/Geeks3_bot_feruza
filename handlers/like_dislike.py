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
from keyboards.like_dislike import like_dislike
from keyboards.start import start_menu_keyboard

router = Router()

@router.callback_query(lambda call: call.data == "view_profiles")
async def random_profiles_call(call: types.CallbackQuery, db=AsyncDataBase()):

    if call.message.caption.startswith("Nickname"):
        await call.message.delete()
    profiles = await db.execute_query(
        query=sql_queries.READ_ALL_PROFILES,
        params=(
            call.from_user.id,
            call.from_user.id
        ),
        fetch="All"
    )

    if profiles:
        random_profile = random.choice(profiles)
        photo = types.FSInputFile(random_profile["PHOTO"])

        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname = random_profile['NICKNAME'],
                phone_number = random_profile['PHONE_NUMBER'],
                e_mail = random_profile['EMAIL'],
                bio = random_profile['BIO'],
            ),
            reply_markup = await like_dislike(tg_id=random_profile["TELEGRAM_ID"])
        )

        print(profiles)
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text = "Вы уже лайкнули все профили, заходите позже!"
        )



@router.callback_query(lambda call: "like_" in call.data)
async def like_detect_call(call: types.CallbackQuery, db=AsyncDataBase()):
    owner_tg_id = call.data.replace("like_", "")
    await db.execute_query(
        query=sql_queries.INSERT_LIKE_TABLE,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            1
        ),
        fetch="None"
    )

    await random_profiles_call(call=call)



@router.callback_query(lambda call: call.data == "dislike")
async def dislike_detect_call(call: types.CallbackQuery, db=AsyncDataBase()):
    owner_tg_id = call.data.replace("dislike", "")
    await db.execute_query(
        query=sql_queries.INSERT_DISLIKE_TABLE,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            0
        ),
        fetch="None"
    )

    await random_profiles_call(call=call)