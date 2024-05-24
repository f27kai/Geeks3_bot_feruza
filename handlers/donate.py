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
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class DonateStatesGroup(StatesGroup):
    amount = State()
@router.callback_query(lambda call: "donate_" in call.data)
async def detect_donate_call(call: types.CallbackQuery, state: FSMContext, db=AsyncDataBase()):
    recipient_id = call.data.replace("donate_", "")
    donate_user = await db.execute_query(
        query=sql_queries.READ_ALL_USER_TABLE,
        params=(
            call.from_user.id,
        ),
        fetch="One"
    )
    print(donate_user)
    await bot.send_message(
        chat_id=call.from_user.id,
        text="How much do you want to donate? \n"
             f"Your balance: {donate_user['BALANCE']}",
    )

    await state.update_data(owner_id=recipient_id)
    await state.update_data(balance_limit=donate_user['BALANCE'])
    await state.set_state(DonateStatesGroup.amount)


@router.message(DonateStatesGroup.amount)
async def process_donate_amount(message: types.Message, state: FSMContext, db=AsyncDataBase()):
    data = await state.get_data()
    try:
        if int(message.text) < 1:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Please send more than 1 dollar"
            )

            await state.clear()
            return

        elif int(message.text) <= data['balance_limit']:
            await db.execute_query(
                query=sql_queries.UPDATE_SENDER_USER_BALANCE,
                params=(
                    int(message.text),
                    message.from_user.id,
                ),
                fetch="None"
            )

            await db.execute_query(
                query=sql_queries.UPDATE_RECIPIENT_USER_BALANCE,
                params=(
                    int(message.text),
                    data['owner_id'],
                ),
                fetch="None"
            )

            await db.execute_query(
                query=sql_queries.INSERT_DONATE_TRANSACTIONS_TABLE,
                params=(
                    None,
                    message.from_user.id,
                    data['owner_id'],
                    int(message.text),
                ),
                fetch="None"
            )

            await bot.send_message(
                chat_id=data['owner_id'],
                text=f"Someone sent to you donate\n"
                     f"Amount of donate: {message.text}"
            )

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Donate transactions sent successfully"
            )

        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Not enough balance to donate {data['balance_limit']}"
            )

            await state.clear()
            return

    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Please use numeric answer"
        )

        await state.clear()
        return

