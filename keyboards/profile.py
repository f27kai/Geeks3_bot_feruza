from aiogram import Dispatcher
from aiogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
)



async def my_profile():
    update_button = InlineKeyboardButton(
        text = "Update Profile",
        callback_data="update_profile"
    )

    delete_button = InlineKeyboardButton(
        text = "Delete Profile",
        callback_data="delete"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [update_button],
            [delete_button],
        ]
    )
    return markup