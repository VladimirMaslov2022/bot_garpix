import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F

from app.handlers import router

load_dotenv(".env")

async def main():
    bot = Bot(token = '7723499886:AAG2CLb2M91uw8OtwrVazI5d9tC2XM2SKqM')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is turned off')
