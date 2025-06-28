import emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def welcome() -> InlineKeyboardMarkup:
    buttons = InlineKeyboardBuilder()
    city_button = InlineKeyboardButton(text=f"{emoji.emojize('🔍')} Поиск",
                                       callback_data="search")
    cmd_help = InlineKeyboardButton(text=f"{emoji.emojize('⚠️')} /help", callback_data="help")
    buttons.row(city_button)
    buttons.row(cmd_help)
    return buttons.as_markup(resize_keyboard=True)
