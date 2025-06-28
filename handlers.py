from datetime import datetime, date

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards import welcome
from kudagoapi import get_cinema_events

router = Router()

CITYLIST = {
    "Санкт-Петербург": "spb",
    "Москва": "msk",
    "Новосибирск": "novosibirsk",
    "Екатеринбург": "ekaterinburg",
    "Нижний Новгород": "nizhniy-novgorod",
    "Казань": "kazan",
    "Выборг": "vyborg",
    "Самара": "samara",
    "Краснодар": "krasnodar",
    "Сочи": "sochi",
    "Уфа": "ufa",
    "Красноярск": "krasnoyarsk"
}


class Form(StatesGroup):
    city = State()
    date = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Привет! 👋 Это GoCinemaBot 🎥'
        '\nЯ помогу тебе найти самый удобный киносеанс,'
        '\nнажми на кнопку "🔍 Поиск" и скорее на фильм!',
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
    await state.update_data(user_city=user_city)
    await state.set_state(Form.date)
    await message.answer('✅ Отлично! Теперь введите дату, когда хотите пойти в кино')


@router.message(Form.date)
async def process_date(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_city = user_data["user_city"]
    input_text = message.text.strip()
    kudago_city = CITYLIST.get(user_city)
    try:
        pars_date = datetime.strptime(input_text, "%Y-%m-%d")
        if pars_date.date() < date.today():
            await message.answer("❌ Мы, пока что, не можем вернуться в прошлое 🥲")
        else:
            await message.answer('✅ Отлично! Сейчас покажем результаты поиска')
    except ValueError:
        await message.answer("❌ Введите дату в указанном формате дд.мм.гг")
        return
    formatted_date = pars_date.strftime("%Y-%m-%d")

    try:
        events = await get_cinema_events(kudago_city, formatted_date)
    except Exception as e:
        await message.answer(f"❌ Ошибка при запросе к API: {e}")
        await state.clear()
        return
    if not events:
        await message.answer("😕 Киносеансы не найдены на выбранную дату.")
    else:
        for movie in events:
            title = movie.get("title", "Без названия")
            place = movie.get("place") or {}
            place_title = place.get("title", "Место не указано")
            await message.answer(f"🎬 {title}\n📍 {place_title}")
    import json

    if events:
        debug = json.dumps(events[0], indent=2, ensure_ascii=False)
        await message.answer(f"🔍 Первый элемент ответа:\n<pre>{debug}</pre>", parse_mode="HTML")
    else:
        await message.answer("❌ Ничего не пришло от API.")

    await state.clear()
