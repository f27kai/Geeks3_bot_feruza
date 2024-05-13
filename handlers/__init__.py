from aiogram import types, Dispatcher, Router
from . import (
    start,
    registration,
    profile,
    like_dislike,
    reverence
)


def setup_routes() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)
    router.include_router(profile.router)
    router.include_router(like_dislike.router)
    router.include_router(reverence.router)

    return router
