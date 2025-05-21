import asyncio, os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from logger import logger

load_dotenv(dotenv_path='config.env')
logger.info('LOGGING ON')
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
