import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 1,
    "lesson_code": "HSK1-L01",
    "title": "你好",
    "goal": "Learn how to greet people and apologize in Chinese",
    "intro_text": (
        "In the first lesson you will learn Chinese greetings. "
        "This lesson includes 6 new words, 3 dialogues, and basic pronunciation rules."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "你",    "pinyin": "nǐ",        "pos": "pron.", "meaning": "you (singular)"},
        {"no": 2, "zh": "好",    "pinyin": "hǎo",       "pos": "adj.",  "meaning": "good, great"},
        {"no": 3, "zh": "您",    "pinyin": "nín",       "pos": "pron.", "meaning": "you (formal/polite)"},
        {"no": 4, "zh": "你们",  "pinyin": "nǐmen",     "pos": "pron.", "meaning": "you (plural)"},
        {"no": 5, "zh": "对不起","pinyin": "duìbuqǐ",   "pos": "v.",    "meaning": "sorry, excuse me"},
        {"no": 6, "zh": "没关系","pinyin": "méi guānxi","pos": "expr.", "meaning": "no problem, don't worry"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Tanishlar uchrashadi",
            "dialogue": [
                {"speaker": "A", "zh": "你好！",  "pinyin": "Nǐ hǎo!",   "translation": "Hello!"},
                {"speaker": "B", "zh": "你好！",  "pinyin": "Nǐ hǎo!",   "translation": "Hello!"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Hurmatli salomlashuv",
            "dialogue": [
                {"speaker": "A", "zh": "您好！",   "pinyin": "Nín hǎo!",    "translation": "Hello (formal)!"},
                {"speaker": "B", "zh": "你们好！", "pinyin": "Nǐmen hǎo!",  "translation": "Hello everyone!"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kechirim so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "对不起！", "pinyin": "Duìbuqǐ!",      "translation": "Sorry!"},
                {"speaker": "B", "zh": "没关系！", "pinyin": "Méi guānxi!",   "translation": "No problem!"},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "四声 — To'rt ton",
            "explanation": (
                "In Chinese, every syllable has 4 tones:\n"
                "Tone 1 (—): flat and high — mā (mother)\n"
                "Tone 2 (ˊ): rising — má (hemp plant)\n"
                "Tone 3 (ˇ): falling then rising — mǎ (horse)\n"
                "Tone 4 (ˋ): falling — mà (to scold)\n\n"
                "Tone changes the meaning!"
            ),
            "examples": [
                {"zh": "妈", "pinyin": "mā", "meaning": "mother (tone 1)"},
                {"zh": "马", "pinyin": "mǎ", "meaning": "horse (tone 3)"},
                {"zh": "骂", "pinyin": "mà", "meaning": "to scold (tone 4)"},
            ]
        },
        {
            "no": 2,
            "title_zh": "变调 — Ton o'zgarishi (3+3)",
            "explanation": (
                "When two tone-3 syllables appear in a row, the first changes to tone 2.\n"
                "3+3 → 2+3\n"
                "Example: 你(nǐ) + 好(hǎo) → nī hǎo (but written: nǐ hǎo)"
            ),
            "examples": [
                {"zh": "你好", "pinyin": "nī hǎo → nǐ hǎo", "meaning": "hello (written nǐ hǎo)"},
                {"zh": "可以", "pinyin": "ké yǐ → kě yǐ",   "meaning": "may, can"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Hello! (casual)",          "answer": "你好！",   "pinyin": "Nǐ hǎo!"},
                {"prompt": "Hello! (formal)",          "answer": "您好！",   "pinyin": "Nín hǎo!"},
                {"prompt": "Sorry!",                   "answer": "对不起！", "pinyin": "Duìbuqǐ!"},
                {"prompt": "No problem!",              "answer": "没关系！", "pinyin": "Méi guānxi!"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "A: 你___！  B: 你好！",     "answer": "好", "pinyin": "hǎo"},
                {"prompt": "A: 对不起！  B: ___！",     "answer": "没关系", "pinyin": "méi guānxi"},
                {"prompt": "一个老师对很多学生说: ___好！", "answer": "你们", "pinyin": "nǐmen"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你好！", "您好！", "对不起！", "没关系！"]},
        {"no": 2, "answers": ["好", "没关系", "你们"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 2 dialogues using the following words (written):",
            "words": ["你好", "您好", "对不起", "没关系"],
            "example": "A: 对不起！B: 没关系！",
        },
        {
            "no": 2,
            "instruction": "Practice the tones and say them aloud:",
            "words": [
                {"zh": "妈", "pinyin": "mā", "meaning": "mother"},
                {"zh": "马", "pinyin": "mǎ", "meaning": "horse"},
                {"zh": "骂", "pinyin": "mà", "meaning": "to scold"},
            ]
        }
    ], ensure_ascii=False),

    "is_active": True,
}


async def seed():
    async with SessionLocal() as session:
        existing = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        if existing.scalar_one_or_none():
            print(f"Lesson {LESSON['lesson_code']} already exists, skipping.")
            return

        lesson = CourseLesson(**LESSON)
        session.add(lesson)
        await session.commit()
        print(f"✅ Lesson {LESSON['lesson_code']} — {LESSON['title']} created.")


if __name__ == "__main__":
    asyncio.run(seed())
