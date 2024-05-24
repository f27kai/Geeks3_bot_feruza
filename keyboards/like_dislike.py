from aiogram import Dispatcher
from aiogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
)



async def like_dislike(tg_id):
    like_button = InlineKeyboardButton(
        text = "Like",
        callback_data=f"like_{tg_id}"
    )

    dislike_button = InlineKeyboardButton(
        text = "Dislike",
        callback_data="dislike"
    )

    donate_button = InlineKeyboardButton(
        text="Donate",
        callback_data=f"donate_{tg_id}"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [like_button],
            [dislike_button],
            [donate_button],
        ]
    )
    return markup


async def history(tg_id):
    donate_button = InlineKeyboardButton(
        text="Donate",
        callback_data=f"donate_{tg_id}"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [donate_button],
        ]
    )
    return markup