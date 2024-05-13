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
from keyboards.profile import my_profile
from keyboards.start import start_menu_keyboard

router = Router()

@router.callback_query(lambda call: call.data == "profile")
async def profiles(call: types.CallbackQuery, db=AsyncDataBase()):
    profile = await db.execute_query(
        query=sql_queries.READ_PROFLE_TABLE,
        params=(
            call.from_user.id,
        ),
        fetch="One"
    )


    if profile:
        photo = types.FSInputFile(profile["PHOTO"])

        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname=profile['NICKNAME'],
                phone_number=profile['PHONE_NUMBER'],
                e_mail=profile['EMAIL'],
                bio=profile['BIO'],
            ),
            reply_markup=await my_profile()
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Вы не зарегистрировались"
        )


@router.callback_query(lambda call: call.data == "delete")
async def delete_profiles(call: types.CallbackQuery, db=AsyncDataBase()):
    await db.execute_query(
        query=sql_queries.DELETE_PROFILE,
        params=(
            call.from_user.id,
        ),
        fetch="None"
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text = "Профиль успешно удален!"
    )