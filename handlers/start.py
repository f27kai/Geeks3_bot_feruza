import sqlite3

from aiogram import Router, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import chat
from aiogram.utils.deep_linking import create_start_link

from config import bot, ADMIN_ID, MEDIA_PATH
from database.a_db import AsyncDataBase
from database import sql_queries
from const import START_MENU_TEXT
from keyboards.start import start_menu_keyboard
from scraper.news_scraper import NewsScraper

router = Router()

@router.message(Command('start'))
async def start(message: types.Message, db=AsyncDataBase()):

    command = message.text
    token = command.split()

    if len(token) > 1:
        await process_reverence_link(token[1], message)

    try:
        await db.execute_query(
            query=sql_queries.INSERT_USER_TABLE,
            params=(
                None,
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                None,
                0
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


async def process_reverence_link(token, message, db=AsyncDataBase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
            query=sql_queries.READ_USER_TABLE_BY_LINK,
            params=(
                link,
            ),
            fetch = "One"
        )

    if owner["TELEGRAM_ID"] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text = "You can not use your own link"
        )
        return

    try:
        await db.execute_query(
            query=sql_queries.INSERT_REVERENCE_USER,
            params=(
                None,
                owner["TELEGRAM_ID"],
                message.from_user.id,
            ),
            fetch="None"
        )

        await db.execute_query(
            query=sql_queries.UPDATE_REVERENCE_USER_BALANCE,
            params=(
                owner["TELEGRAM_ID"],
            ),
            fetch="None"
        )

        await bot.send_message(
            chat_id=owner["TELEGRAM_ID"],
            text = "Вы получили свой КЭШБЭК!\n"
                   "Поздравляем!"
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ты уже использовал эту линк"
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


@router.callback_query(lambda call: call.data == "news")
async def laters_news_links(call: types.CallbackQuery, db=AsyncDataBase()):
    scraper = NewsScraper()
    data = scraper.scrape_data()
    for i in data:
        dorams_link = await db.execute_query(
            query=sql_queries.READ_DORAMS_TABLE,
            params=(
                i,
            ),
            fetch="All"
        )
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="https://dorama.land" + i
        )

        if not dorams_link:
            await db.execute_query(
                query=sql_queries.INSERT_DORAM_TABLE,
                params=(
                    None,
                    i
                ),
                fetch="None"
            )


