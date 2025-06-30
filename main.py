import asyncio, os
from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv

from app.logger import log_info
from app.handlers import router

load_dotenv(".env")


async def main():
    log_info('Starting bot initialization')
    global bot
    bot = Bot(token = os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    log_info('Bot initialized successfully')
            #  , 
            #     bot_id=bot.id, 
            #     bot_name=(await bot.get_me()).username)
    await dp.start_polling(bot) # skip_updates=True


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info('Bot is turned off') # 'MAIN',
        print('Bot is turned off')
