from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.services.onboarding_service import OnboardingService
from app.bot.utils.i18n import t
from app.bot.keyboards.onboarding import language_keyboard, level_keyboard
from app.bot.fsm.onboarding import OnboardingStates


router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    state: FSMContext,
    session,
    command: CommandObject,
):
    service = OnboardingService(session)
    first_name = message.from_user.first_name if message.from_user and message.from_user.first_name else "Friend"

    referral_code = command.args if command and command.args else None

    user, created = await service.get_or_create_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name if message.from_user else None,
        referral_code=referral_code,
    )

    await state.clear()

    if not created and user.language and user.level:
        await message.answer(
            t("welcome_back", user.language, name=first_name)
        )
        return

    onboarding_msg = await message.answer(
        f"{t('welcome', user.language, name=first_name)}\n\n{t('choose_language', user.language)}",
        reply_markup=language_keyboard(),
    )

    await state.update_data(
        onboarding_message_id=onboarding_msg.message_id,
        first_name=first_name,
    )
    await state.set_state(OnboardingStates.choosing_language)


@router.callback_query(OnboardingStates.choosing_language)
async def process_language(callback: CallbackQuery, state: FSMContext, session):
    lang = callback.data.split(":")[1]

    service = OnboardingService(session)

    user, _ = await service.get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name if callback.from_user else None,
    )
    user.language = lang
    await session.commit()

    await callback.answer()

    data = await state.get_data()
    onboarding_message_id = data.get("onboarding_message_id")
    first_name = data.get("first_name", "Friend")

    try:
        if onboarding_message_id:
            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=onboarding_message_id,
                text=f"{t('welcome', lang, name=first_name)}\n\n{t('choose_level', lang)}",
                reply_markup=level_keyboard(lang),
            )
    except Exception:
        pass

    await state.update_data(lang=lang)
    await state.set_state(OnboardingStates.choosing_level)


def _get_demo_lesson(level: str, lang: str) -> str:
    lessons = {
        "beginner": {
            "tj": (
                "🎯 <b>Дарси аввал — Салом гуфтан</b>\n\n"
                "🇨🇳 <b>你好</b> — <i>Nǐ hǎo</i> — Салом\n"
                "🇨🇳 <b>谢谢</b> — <i>Xièxiè</i> — Ташаккур\n"
                "🇨🇳 <b>再见</b> — <i>Zàijiàn</i> — Хайр\n\n"
                "💬 Ҳоло ба бот бинависед: <b>你好 чӣ маъно дорад?</b>"
            ),
            "uz": (
                "🎯 <b>Birinchi dars — Salomlashish</b>\n\n"
                "🇨🇳 <b>你好</b> — <i>Nǐ hǎo</i> — Salom\n"
                "🇨🇳 <b>谢谢</b> — <i>Xièxiè</i> — Rahmat\n"
                "🇨🇳 <b>再见</b> — <i>Zàijiàn</i> — Xayr\n\n"
                "💬 Endi botga yozing: <b>你好 nima degani?</b>"
            ),
            "ru": (
                "🎯 <b>Первый урок — Приветствие</b>\n\n"
                "🇨🇳 <b>你好</b> — <i>Nǐ hǎo</i> — Привет\n"
                "🇨🇳 <b>谢谢</b> — <i>Xièxiè</i> — Спасибо\n"
                "🇨🇳 <b>再见</b> — <i>Zàijiàn</i> — Пока\n\n"
                "💬 Напишите боту: <b>что значит 你好?</b>"
            ),
        },
        "hsk1": {
            "tj": (
                "🎯 <b>Дарси аввал — Рақамҳо</b>\n\n"
                "🇨🇳 <b>一</b> yī — 1 &nbsp;&nbsp; <b>二</b> èr — 2 &nbsp;&nbsp; <b>三</b> sān — 3\n"
                "🇨🇳 <b>四</b> sì — 4 &nbsp;&nbsp; <b>五</b> wǔ — 5 &nbsp;&nbsp; <b>十</b> shí — 10\n\n"
                "💬 Ба бот бинависед: <b>چӣ тавр бигӯям «ман 20 сол дорам»?</b>"
            ),
            "uz": (
                "🎯 <b>Birinchi dars — Raqamlar</b>\n\n"
                "🇨🇳 <b>一</b> yī — 1 &nbsp;&nbsp; <b>二</b> èr — 2 &nbsp;&nbsp; <b>三</b> sān — 3\n"
                "🇨🇳 <b>四</b> sì — 4 &nbsp;&nbsp; <b>五</b> wǔ — 5 &nbsp;&nbsp; <b>十</b> shí — 10\n\n"
                "💬 Botga yozing: <b>«men 20 yoshdaman» xitoycha qanday?</b>"
            ),
            "ru": (
                "🎯 <b>Первый урок — Числа</b>\n\n"
                "🇨🇳 <b>一</b> yī — 1 &nbsp;&nbsp; <b>二</b> èr — 2 &nbsp;&nbsp; <b>三</b> sān — 3\n"
                "🇨🇳 <b>四</b> sì — 4 &nbsp;&nbsp; <b>五</b> wǔ — 5 &nbsp;&nbsp; <b>十</b> shí — 10\n\n"
                "💬 Напишите боту: <b>как сказать «мне 20 лет»?</b>"
            ),
        },
        "hsk2": {
            "tj": (
                "🎯 <b>Дарси аввал — Вақт</b>\n\n"
                "🇨🇳 <b>现在几点？</b> — <i>Xiànzài jǐ diǎn?</i>\n"
                "— Ҳоло соат чанд?\n\n"
                "🇨🇳 <b>今天星期几？</b> — <i>Jīntiān xīngqī jǐ?</i>\n"
                "— Имрӯз рӯзи ҳафта чанд?\n\n"
                "💬 Ба бот бинависед: <b>«Фардо душанбе» хитоӣ чӣ мешавад?</b>"
            ),
            "uz": (
                "🎯 <b>Birinchi dars — Vaqt</b>\n\n"
                "🇨🇳 <b>现在几点？</b> — <i>Xiànzài jǐ diǎn?</i>\n"
                "— Hozir soat necha?\n\n"
                "🇨🇳 <b>今天星期几？</b> — <i>Jīntiān xīngqī jǐ?</i>\n"
                "— Bugun haftaning nechanchi kuni?\n\n"
                "💬 Botga yozing: <b>«Ertaga dushanba» xitoycha qanday?</b>"
            ),
            "ru": (
                "🎯 <b>Первый урок — Время</b>\n\n"
                "🇨🇳 <b>现在几点？</b> — <i>Xiànzài jǐ diǎn?</i>\n"
                "— Который сейчас час?\n\n"
                "🇨🇳 <b>今天星期几？</b> — <i>Jīntiān xīngqī jǐ?</i>\n"
                "— Какой сегодня день недели?\n\n"
                "💬 Напишите боту: <b>как сказать «завтра понедельник»?</b>"
            ),
        },
        "hsk3": {
            "tj": (
                "🎯 <b>Дарси аввал — Эҳсосот</b>\n\n"
                "🇨🇳 <b>我很高兴认识你</b>\n"
                "<i>Wǒ hěn gāoxìng rènshi nǐ</i>\n"
                "— Аз шинос шудан бо шумо хурсандам\n\n"
                "💬 Ба бот бинависед: <b>ин ҷумларо тавзеҳ деҳ ва мисоли дигар биёр</b>"
            ),
            "uz": (
                "🎯 <b>Birinchi dars — His-tuyg'ular</b>\n\n"
                "🇨🇳 <b>我很高兴认识你</b>\n"
                "<i>Wǒ hěn gāoxìng rènshi nǐ</i>\n"
                "— Siz bilan tanishganimdan xursandman\n\n"
                "💬 Botga yozing: <b>bu jumlani tushuntir va boshqa misol keltir</b>"
            ),
            "ru": (
                "🎯 <b>Первый урок — Эмоции</b>\n\n"
                "🇨🇳 <b>我很高兴认识你</b>\n"
                "<i>Wǒ hěn gāoxìng rènshi nǐ</i>\n"
                "— Рад с вами познакомиться\n\n"
                "💬 Напишите боту: <b>объясни это предложение и дай ещё примеры</b>"
            ),
        },
        "hsk4": {
            "tj": (
                "🎯 <b>Дарси аввал — Ибораҳои расмӣ</b>\n\n"
                "🇨🇳 <b>请多关照</b> — <i>Qǐng duō guānzhào</i>\n"
                "— Лутфан мадад кунед (ибораи расмӣ)\n\n"
                "🇨🇳 <b>麻烦你了</b> — <i>Máfan nǐ le</i>\n"
                "— Ба шумо мушкилӣ овардам\n\n"
                "💬 Ба бот бинависед: <b>кай истифода мешаванд ин иборахо?</b>"
            ),
            "uz": (
                "🎯 <b>Birinchi dars — Rasmiy iboralar</b>\n\n"
                "🇨🇳 <b>请多关照</b> — <i>Qǐng duō guānzhào</i>\n"
                "— Iltimos yordam bering (rasmiy ibora)\n\n"
                "🇨🇳 <b>麻烦你了</b> — <i>Máfan nǐ le</i>\n"
                "— Sizni bezovta qildim\n\n"
                "💬 Botga yozing: <b>bu iboralar qachon ishlatiladi?</b>"
            ),
            "ru": (
                "🎯 <b>Первый урок — Формальные выражения</b>\n\n"
                "🇨🇳 <b>请多关照</b> — <i>Qǐng duō guānzhào</i>\n"
                "— Прошу вашей поддержки (формальное)\n\n"
                "🇨🇳 <b>麻烦你了</b> — <i>Máfan nǐ le</i>\n"
                "— Я вас побеспокоил\n\n"
                "💬 Напишите боту: <b>когда используются эти выражения?</b>"
            ),
        },
    }

    level_key = level.lower().replace(" ", "")
    lang_key = lang if lang in ("tj", "uz", "ru") else "ru"

    level_map = {
        "beginner": "beginner",
        "az0": "beginner",
        "hsk1": "hsk1",
        "hsk2": "hsk2",
        "hsk3": "hsk3",
        "hsk4": "hsk4",
    }
    mapped = level_map.get(level_key, "beginner")
    return lessons.get(mapped, {}).get(lang_key, "")


@router.callback_query(OnboardingStates.choosing_level)
async def process_level(callback: CallbackQuery, state: FSMContext, session):
    level = callback.data.split(":")[1]

    service = OnboardingService(session)

    user, _ = await service.get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name if callback.from_user else None,
    )
    user.level = level
    user.learning_mode = "qa"
    await session.commit()

    await callback.answer()

    data = await state.get_data()
    onboarding_message_id = data.get("onboarding_message_id")

    try:
        if onboarding_message_id:
            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=onboarding_message_id,
                text=t("level_saved_explained", user.language),
            )
    except Exception:
        pass

    # First demo lesson based on level
    demo = _get_demo_lesson(level, user.language)
    if demo:
        await callback.message.answer(demo, parse_mode="HTML")

    await callback.message.answer(t("trial_started_info", user.language))
    await callback.message.answer(t("send_first_message", user.language))
    await state.clear()
