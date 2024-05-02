import asyncio
from config import dp, bot
from handlers import setup_routes

async def main():
    router = setup_routes()
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
