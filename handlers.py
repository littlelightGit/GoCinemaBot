
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import welcome
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

router = Router()

CITYLIST = ["Санкт-Петербург", "Москва", "Новосибирск", "Екатеринбург", "Нижний Новгород", "Казань",
            "Выборг", "Самара", "Краснодар", "Сочи", "Уфа", "Красноярск"]

class Form(StatesGroup):
    city = State()
    date = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет! 👋 Это GoCinemaBot 🎥'
        f'\nЯ помогу тебе найти самый удобный киносеанс,'
        f'\nнажми на кнопку "🔍 Поиск" и скорее на фильм!',
        reply_markup=welcome())

@router.callback_query(F.data == "search")
async def sh_cb(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text="🌍 Выбери свой город: Санкт-Петербург, Москва,"
                                       "\nНовосибирск, Екатеринбург, Нижний Новгород,"
                                       "\nКазань, Выборг, Самара, Краснодар,"
                                       "\nСочи, Уфа, Красноярск")
    await state.set_state(Form.city)
    await callback.answer()

@router.message(Form.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    user_city = message.text.strip()

    if user_city not in CITYLIST:
        await message.answer('Введите город из списка доступных')
        return
    await state.set_state(Form.date)






