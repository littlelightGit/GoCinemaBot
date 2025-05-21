import emoji
from keyboards import welcome
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет! {emoji.emojize(':grinning_face_with_smiling_eyes:')}\nЭто GoCinemaBot {emoji.emojize(':cinema:')}\n'
        f'Я помогу тебе найти самый удобный киносеанс! {emoji.emojize(':thumbs_up:')}'
        f'\nНажми на одну из нужных тебе кнопок {emoji.emojize('👀')}\nили воспользуйся командой  /help',
        reply_markup=welcome())
