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
from aiogram.fsm import state
from const import PROFILE_TEXT
from database.sql_queries import READ_PROFLE_TABLE
from keyboards.start import start_menu_keyboard

router = Router()


class SendMoneyStatesGroup(StatesGroup):
    waiting_for_id = State()
    waiting_for_amount = State()
@router.callback_query(lambda call: call.data == "Sendmoney")
async def send_money_wallet(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Введите ID пользователя, которому хотите отправить деньги: "
    )
    await state.set_state(SendMoneyStatesGroup.waiting_for_id)


@router.message(SendMoneyStatesGroup.waiting_for_id)
async def process_user_id(message: types.Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Теперь введите сумму денег для отправки: "
    )

    data = await state.get_data()
    print(data)
    await state.set_state(SendMoneyStatesGroup.waiting_for_amount)


@router.message(SendMoneyStatesGroup.waiting_for_amount)
async def process_send_money_wallet(message: types.Message, state: FSMContext, db=AsyncDataBase()):
    data = await state.get_data()
    try:
        amount = float(message.text)
        if amount < 1:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Сумма должна быть больше 1 доллара"
            )
            return

        user_id = data['user_id']
        user_id = int(user_id)
        recipient_user = await db.execute_query(
            query=sql_queries.READ_ALL_ID_USER_TABLE,
            params=(
                user_id,
            ),
            fetch="One"
        )
        print(f"Recipient user query result: {recipient_user}")

        if recipient_user:
            await db.execute_query(
                query=sql_queries.UPDATE_SENDER_ID_USER_BALANCE,
                params=(
                    amount,
                    message.from_user.id
                ),
                fetch="None"
            )

            await db.execute_query(
                query=sql_queries.UPDATE_RECIPIENT_ID_USER_BALANCE,
                params=(
                    amount,
                    user_id
                ),
                fetch="None"
            )

            await db.execute_query(
                query=sql_queries.INSERT_SEND_MONEY_TRANSACTIONS_TABLE,
                params=(
                    None,
                    message.from_user.id,
                    data['user_id'],
                    amount
                ),
                fetch="None"
            )

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Транзакция успешно выполнена. \n"
                     f"Сумма: {amount},\n"
                     f"получатель: {data['user_id'], recipient_user['FIRST_NAME']}"
            )

            await bot.send_message(
                chat_id=recipient_user['TELEGRAM_ID'],
                text=f"Someone sent to you donate\n"
                     f"Amount of donate: {amount}"
            )

        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Пользователь с указанным ID не найден"
            )

    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Пожалуйста, введите корректную сумму"
        )