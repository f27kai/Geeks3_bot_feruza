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

    reverence_button = InlineKeyboardButton(
        text="Reverence menu",
        callback_data="reverence_menu"
    )


    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profile_user],
            [profiles_button],
            [reverence_button],
        ]
    )
    return markup