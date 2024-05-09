from aiogram import Dispatcher
from aiogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
)



async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text = "Registration",
        callback_data="registration"
    )

    profile_user = InlineKeyboardButton(
        text = "My profile",
        callback_data="profile"
    )

    profiles_button = InlineKeyboardButton(
        text="View profiles",
        callback_data="view_profiles"
    )

    proverka = InlineKeyboardButton(
        text="proverka",
        callback_data="proverka"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profile_user],
            [profiles_button],
            [proverka],
        ]
    )
    return markup