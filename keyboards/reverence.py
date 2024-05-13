from aiogram import Dispatcher
from aiogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
)



async def reverence_menu_keyboards():
    link_button = InlineKeyboardButton(
        text = "Link",
        callback_data="reverence_link",
    )

    balance_button = InlineKeyboardButton(
        text = "Balance",
        callback_data="reverence_balance",
    )

    reference_user_button = InlineKeyboardButton(
        text="List of references",
        callback_data="reverence_list",
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [balance_button],
            [reference_user_button],
        ]
    )
    return markup