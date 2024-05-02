import asyncio
from config import dp, bot
from handlers import setup_routes
from database.a_db import AsyncDataBase

async def main():
    db = AsyncDataBase()
    await db.create_db()
    router = setup_routes()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
