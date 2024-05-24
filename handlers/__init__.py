from aiogram import types, Dispatcher, Router
from . import (
    start,
    registration,
    profile,
    like_dislike,
    reverence,
    donate,
    like_history,
    wallet_id,
    send_donate
)


def setup_routes() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)
    router.include_router(profile.router)
    router.include_router(like_dislike.router)
    router.include_router(reverence.router)
    router.include_router(donate.router)
    router.include_router(like_history.router)
    router.include_router(wallet_id.router)
    router.include_router(send_donate.router)

    return router
