from aiogram import types, Dispatcher, Router


def setup_routes() -> Router:
    from . import (
        start,
        registration
    )
    router = Router()
    router.include_router(start.router)
    router.include_router(registration.router)

    return router
