from datetime import datetime, date
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
async def process_city(message: Message, state: FSMContext):
    user_city = message.text.strip()

    if user_city not in CITYLIST:
        await message.answer('❌ Введите город из списка доступных')
        return
    await state.update_data(citys=user_city)
    await state.set_state(Form.date)
    await message.answer('✅ Отлично! Теперь введите дату, когда хотите пойти в кино')


@router.message(Form.date)
async def process_date(message: Message, state: FSMContext):
    user_date = message.text.strip()
    try:
        pars_date = datetime.strptime(user_date, "%d.%m.%y")
        if pars_date.date() < date.today():
            await message.answer("❌ Мы, пока что, не можем вернуться в прошлое 🥲")
        else:
            await message.answer('✅ Отлично! Сейчас покажем результаты поиска')
    except ValueError:
        await message.answer("❌ Введите дату в указанном формате дд.мм.гг")


