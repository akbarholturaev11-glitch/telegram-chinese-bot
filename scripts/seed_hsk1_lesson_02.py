import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 2,
    "lesson_code": "HSK1-L02",
    "title": "谢谢你",
    "goal": "Learn how to express gratitude and say goodbye in Chinese",
    "intro_text": (
        "In the second lesson you will learn how to express gratitude and say goodbye in Chinese. "
        "4 new words, 3 dialogues, and the rules for the neutral tone."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "谢谢",   "pinyin": "xièxie",  "pos": "v.",   "meaning": "to thank, thank you"},
        {"no": 2, "zh": "不",     "pinyin": "bù",       "pos": "adv.", "meaning": "no, not"},
        {"no": 3, "zh": "不客气", "pinyin": "bú kèqi",  "pos": "expr.", "meaning": "you're welcome, no problem"},
        {"no": 4, "zh": "再见",   "pinyin": "zàijiàn",  "pos": "v.",   "meaning": "goodbye, see you"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yordam uchun rahmat",
            "dialogue": [
                {"speaker": "A", "zh": "谢谢！", "pinyin": "Xièxie!", "translation": "Thank you!"},
                {"speaker": "B", "zh": "不谢！", "pinyin": "Bú xiè!", "translation": "You're welcome!"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Rasmiy rahmat",
            "dialogue": [
                {"speaker": "A", "zh": "谢谢你！", "pinyin": "Xièxie nǐ!", "translation": "Thank you!"},
                {"speaker": "B", "zh": "不客气！", "pinyin": "Bú kèqi!",   "translation": "You're welcome!"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Xayrlashuv",
            "dialogue": [
                {"speaker": "A", "zh": "再见！", "pinyin": "Zàijiàn!", "translation": "Goodbye!"},
                {"speaker": "B", "zh": "再见！", "pinyin": "Zàijiàn!", "translation": "Goodbye!"},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "不 — Inkor yuklamasi",
            "explanation": (
                "不(bù) — negation particle (no, not).\n"
                "Note: 不 is tone 4, but changes to tone 2 before another tone-4 syllable.\n"
                "bù + tone 4 → bú + tone 4\n"
                "Example: 不客气 → bú kèqi\n"
                "不谢 → bú xiè"
            ),
            "examples": [
                {"zh": "不谢",   "pinyin": "bú xiè",  "meaning": "you're welcome"},
                {"zh": "不客气", "pinyin": "bú kèqi", "meaning": "you're welcome"},
                {"zh": "不好",   "pinyin": "bù hǎo",  "meaning": "not good"},
            ]
        },
        {
            "no": 2,
            "title_zh": "轻声 — Neytral ton",
            "explanation": (
                "Chinese also has a 5th tone — the neutral tone (轻声).\n"
                "It is short and light, with no tone mark.\n"
                "It often appears in kinship terms.\n"
                "Example: 妈妈(māma), 爸爸(bàba), 爷爷(yéye), 奶奶(nǎinai)"
            ),
            "examples": [
                {"zh": "妈妈", "pinyin": "māma",   "meaning": "mother"},
                {"zh": "爸爸", "pinyin": "bàba",   "meaning": "father"},
                {"zh": "爷爷", "pinyin": "yéye",   "meaning": "paternal grandfather"},
                {"zh": "奶奶", "pinyin": "nǎinai", "meaning": "paternal grandmother"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Thank you!",               "answer": "谢谢！",   "pinyin": "Xièxie!"},
                {"prompt": "Thank you (to you)!",      "answer": "谢谢你！", "pinyin": "Xièxie nǐ!"},
                {"prompt": "You're welcome!",           "answer": "不客气！", "pinyin": "Bú kèqi!"},
                {"prompt": "Goodbye!",                  "answer": "再见！",   "pinyin": "Zàijiàn!"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "A: 谢谢你！  B: ___！", "answer": "不客气", "pinyin": "bú kèqi"},
                {"prompt": "A: ___！     B: 再见！", "answer": "再见",   "pinyin": "zàijiàn"},
                {"prompt": "A: 谢谢！    B: ___！",  "answer": "不谢",   "pinyin": "bú xiè"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["谢谢！", "谢谢你！", "不客气！", "再见！"]},
        {"no": 2, "answers": ["不客气", "再见", "不谢"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 2 complete dialogues using the following words:",
            "words": ["谢谢", "不客气", "再见", "你好"],
            "example": "A: 你好！... A: 谢谢！B: 不客气！再见！B: 再见！",
        },
        {
            "no": 2,
            "instruction": "Write the correct pronunciation of 不 (bù or bú):",
            "items": [
                {"prompt": "不好",   "answer": "bù hǎo"},
                {"prompt": "不谢",   "answer": "bú xiè"},
                {"prompt": "不客气", "answer": "bú kèqi"},
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
