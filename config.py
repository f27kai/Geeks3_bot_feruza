from aiogram import Bot, Dispatcher
from decouple import config

TOKEN = config('TOKEN')
ADMIN_ID = config("ADMIN_ID")
bot = Bot(token=TOKEN)
dp = Dispatcher()


