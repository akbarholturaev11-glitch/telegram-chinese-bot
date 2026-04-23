from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.utils.i18n import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
                InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="lang:tj"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
            ]
        ]
    )


def level_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("level_beginner", lang), callback_data="level:beginner")],
            [
                InlineKeyboardButton(text="A1", callback_data="level:a1"),
                InlineKeyboardButton(text="A2", callback_data="level:a2"),
            ],
            [
                InlineKeyboardButton(text="B1", callback_data="level:b1"),
                InlineKeyboardButton(text="B2", callback_data="level:b2"),
            ],
            [
                InlineKeyboardButton(text="C1", callback_data="level:c1"),
            ],
        ]
    )
