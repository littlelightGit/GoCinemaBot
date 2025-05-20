from aiogram import Bot, Dispatcher
import asyncio, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
