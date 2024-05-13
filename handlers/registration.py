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
from database.sql_queries import READ_PROFLE_TABLE
from keyboards.start import start_menu_keyboard

router = Router()




class RegistrationStates(StatesGroup):
    nickname = State()
    phone_number = State()
    e_mail = State()
    bio = State()
    photo = State()

@router.callback_query(lambda call: call.data == "registration")
async def registration(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text = "Пожалуйста, напишите ваш никнейм!"
    )
    await state.set_state(RegistrationStates.nickname)


@router.callback_query(lambda call: call.data == "update_profile")
async def re_registration(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text = "Пожалуйста, напишите ваш никнейм!"
    )
    await state.set_state(RegistrationStates.nickname)

@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Напишите ваш номер!"
    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.phone_number)


@router.message(RegistrationStates.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Напишите ваш адрес электронной почты!"
    )

    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.e_mail)


@router.message(RegistrationStates.e_mail)
async def process_e_mail(message: types.Message, state: FSMContext):
    await state.update_data(e_mail=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Напишите о себе, пожалуйста!"
    )

    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.bio)

@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Отправьте фото!"
    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.photo)


@router.message(RegistrationStates.photo)
async def process_photo(message: types.Message, state: FSMContext, db=AsyncDataBase()):
    file_id  = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    print("media/" + file_path)
    await bot.download_file(
        file_path,
        "media/" + file_path
    )

    data = await state.get_data()
    photo = FSInputFile("media/" + file_path)
    profile = await db.execute_query(
        query=sql_queries.READ_PROFLE_TABLE,
        params=(
            message.from_user.id,
        ),
        fetch="One"
    )
    if profile:
        await db.execute_query(
            query=sql_queries.UPDATE_PROFILE_TABLE,
            params=(
                data['nickname'],
                data['phone_number'],
                data['e_mail'],
                data['bio'],
                "media/" + file_path,
                message.from_user.id
            ),
            fetch="None"
        )

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Вы перезагистрировали, успешно!"
        )
    else:
        await db.execute_query(
            query=sql_queries.INSERT_PROFILE_TABLE,
            params=(
                None,
                message.from_user.id,
                data['nickname'],
                data['phone_number'],
                data['e_mail'],
                data['bio'],
                "media/" + file_path
            ),
            fetch="None"
        )

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Вы зарегистрировали, успешно!"
        )



    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname = data['nickname'],
            phone_number = data['phone_number'],
            e_mail = data['e_mail'],
            bio = data['bio'],
        )
    )





