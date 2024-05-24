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

    like_history_button = InlineKeyboardButton(
        text="Liked profiles",
        callback_data="history"
    )

    wallet_id_button = InlineKeyboardButton(
        text="Wallet ID",
        callback_data="WalletId"
    )

    send_money_button = InlineKeyboardButton(
        text="Send Money",
        callback_data="Sendmoney"
    )

    news_button = InlineKeyboardButton(
        text="News doram 2024",
        callback_data="news"
    )



    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profile_user],
            [profiles_button],
            [reverence_button],
            [like_history_button],
            [wallet_id_button],
            [send_money_button],
            [news_button],
        ]
    )
    return markup