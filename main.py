from aiogram import Bot, Dispatcher
import asyncio


async def main():
    bot = Bot('TOKEN')
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
