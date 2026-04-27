import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 5,
    "lesson_code": "HSK1-L05",
    "title": "她女儿今年二十岁",
    "goal": "Talk about age and family members, and learn numbers up to 100",
    "intro_text": (
        "In the fifth lesson you will learn how to ask and tell someone's age, "
        "talk about the number of family members, and learn numbers up to 100. "
        "10 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "家",   "pinyin": "jiā",     "pos": "n.",    "meaning": "family, home"},
        {"no": 2,  "zh": "有",   "pinyin": "yǒu",     "pos": "v.",    "meaning": "to have, there is"},
        {"no": 3,  "zh": "口",   "pinyin": "kǒu",     "pos": "m.",    "meaning": "measure word for family members"},
        {"no": 4,  "zh": "女儿", "pinyin": "nǚ'ér",   "pos": "n.",    "meaning": "daughter"},
        {"no": 5,  "zh": "几",   "pinyin": "jǐ",      "pos": "pron.", "meaning": "how many (up to 10)"},
        {"no": 6,  "zh": "岁",   "pinyin": "suì",     "pos": "m.",    "meaning": "years old (measure word for age)"},
        {"no": 7,  "zh": "了",   "pinyin": "le",      "pos": "part.", "meaning": "change-of-state particle"},
        {"no": 8,  "zh": "今年", "pinyin": "jīnnián", "pos": "n.",    "meaning": "this year"},
        {"no": 9,  "zh": "多",   "pinyin": "duō",     "pos": "adv.",  "meaning": "many, how (degree)"},
        {"no": 10, "zh": "大",   "pinyin": "dà",      "pos": "adj.",  "meaning": "big, old (in age)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — oila a'zolari",
            "dialogue": [
                {"speaker": "A", "zh": "你家有几口人？",  "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",  "translation": "How many people are in your family?"},
                {"speaker": "B", "zh": "我家有三口人。",  "pinyin": "Wǒ jiā yǒu sān kǒu rén.", "translation": "There are three people in my family."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Ofisda — yosh so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你女儿几岁了？",   "pinyin": "Nǐ nǚ'ér jǐ suì le?",    "translation": "How old is your daughter?"},
                {"speaker": "B", "zh": "她今年四岁了。",   "pinyin": "Tā jīnnián sì suì le.",   "translation": "She is four years old this year."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Ofisda — kattalar yoshi",
            "dialogue": [
                {"speaker": "A", "zh": "李老师多大了？",       "pinyin": "Lǐ lǎoshī duō dà le?",              "translation": "How old is Teacher Li?"},
                {"speaker": "B", "zh": "她今年五十岁了。",     "pinyin": "Tā jīnnián wǔshí suì le.",          "translation": "She is fifty years old this year."},
                {"speaker": "A", "zh": "她女儿呢？",           "pinyin": "Tā nǚ'ér ne?",                      "translation": "What about her daughter?"},
                {"speaker": "B", "zh": "她女儿今年二十岁。",   "pinyin": "Tā nǚ'ér jīnnián èrshí suì.",       "translation": "Her daughter is twenty years old this year."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "几 — Necha? (10 gacha)",
            "explanation": (
                "几(jǐ) — question word for numbers under 10.\n"
                "Structure: Subject + 有 + 几 + Measure word + Noun?\n\n"
                "Example:\n"
                "你家有几口人？— How many people are in your family?\n"
                "你有几个汉语老师？— How many Chinese teachers do you have?\n"
                "你女儿几岁了？— How old is your daughter?"
            ),
            "examples": [
                {"zh": "你家有几口人？",   "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",  "meaning": "How many people are in your family?"},
                {"zh": "你有几个朋友？",   "pinyin": "Nǐ yǒu jǐ ge péngyou?",   "meaning": "How many friends do you have?"},
                {"zh": "她有几岁了？",     "pinyin": "Tā yǒu jǐ suì le?",        "meaning": "How old is she?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "100 gacha raqamlar",
            "explanation": (
                "1-10: 一yī 二èr 三sān 四sì 五wǔ 六liù 七qī 八bā 九jiǔ 十shí\n\n"
                "Tens:\n"
                "20 = 二十 (èrshí)\n"
                "30 = 三十 (sānshí)\n"
                "50 = 五十 (wǔshí)\n"
                "99 = 九十九 (jiǔshíjiǔ)\n\n"
                "Mixed numbers:\n"
                "23 = 二十三 (èrshísān)\n"
                "56 = 五十六 (wǔshíliù)\n"
                "88 = 八十八 (bāshíbā)"
            ),
            "examples": [
                {"zh": "二十",   "pinyin": "èrshí",    "meaning": "20"},
                {"zh": "五十",   "pinyin": "wǔshí",    "meaning": "50"},
                {"zh": "二十三", "pinyin": "èrshísān", "meaning": "23"},
                {"zh": "九十九", "pinyin": "jiǔshíjiǔ","meaning": "99"},
            ]
        },
        {
            "no": 3,
            "title_zh": "了 — O'zgarish yuklamasi",
            "explanation": (
                "了(le) — placed at the end of a sentence indicates a new state or change.\n\n"
                "Example:\n"
                "她今年五十岁了。— She has turned fifty this year (new state).\n"
                "我女儿四岁了。— My daughter has turned four.\n\n"
                "多大了？— How old have you turned? (asking age)"
            ),
            "examples": [
                {"zh": "她今年二十岁了。", "pinyin": "Tā jīnnián èrshí suì le.", "meaning": "She has turned twenty this year."},
                {"zh": "他五十岁了。",     "pinyin": "Tā wǔshí suì le.",         "meaning": "He has turned fifty."},
                {"zh": "你多大了？",       "pinyin": "Nǐ duō dà le?",            "meaning": "How old are you?"},
            ]
        },
        {
            "no": 4,
            "title_zh": "多大 — Yosh so'rash",
            "explanation": (
                "多大(duō dà) — used to ask the age of adults.\n"
                "几岁(jǐ suì) — used to ask the age of children (under 10).\n\n"
                "Adults: 你多大了？— How old are you?\n"
                "Children: 你女儿几岁了？— How old is your daughter?"
            ),
            "examples": [
                {"zh": "你多大了？",     "pinyin": "Nǐ duō dà le?",       "meaning": "How old are you? (adults)"},
                {"zh": "她女儿几岁了？", "pinyin": "Tā nǚ'ér jǐ suì le?", "meaning": "How old is her daughter? (child)"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "numbers",
            "instruction": "Write the numbers in Chinese:",
            "items": [
                {"prompt": "25",  "answer": "二十五",   "pinyin": "èrshíwǔ"},
                {"prompt": "38",  "answer": "三十八",   "pinyin": "sānshíbā"},
                {"prompt": "50",  "answer": "五十",     "pinyin": "wǔshí"},
                {"prompt": "99",  "answer": "九十九",   "pinyin": "jiǔshíjiǔ"},
                {"prompt": "100", "answer": "一百",     "pinyin": "yìbǎi"},
            ]
        },
        {
            "no": 2,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "How many people are in your family?",      "answer": "你家有几口人？",   "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?"},
                {"prompt": "There are five people in our family.",     "answer": "我家有五口人。",   "pinyin": "Wǒ jiā yǒu wǔ kǒu rén."},
                {"prompt": "How old are you?",                          "answer": "你多大了？",       "pinyin": "Nǐ duō dà le?"},
                {"prompt": "She is twenty years old this year.",        "answer": "她今年二十岁了。", "pinyin": "Tā jīnnián èrshí suì le."},
            ]
        },
        {
            "no": 3,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "你家___几口人？",          "answer": "有", "pinyin": "yǒu"},
                {"prompt": "李老师今年五十___了。",     "answer": "岁", "pinyin": "suì"},
                {"prompt": "你女儿___岁了？",           "answer": "几", "pinyin": "jǐ"},
                {"prompt": "李老师___大了？",            "answer": "多", "pinyin": "duō"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["二十五", "三十八", "五十", "九十九", "一百"]},
        {"no": 2, "answers": ["你家有几口人？", "我家有五口人。", "你多大了？", "她今年二十岁了。"]},
        {"no": 3, "answers": ["有", "岁", "几", "多"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 3-4 sentences about your own family:",
            "template": "我家有___口人。我今年___岁了。我___有女儿/儿子。",
            "words": ["家", "有", "口", "岁", "今年", "了"],
        },
        {
            "no": 2,
            "instruction": "Write the numbers in Chinese:",
            "items": [
                {"prompt": "17",  "answer": "十七"},
                {"prompt": "43",  "answer": "四十三"},
                {"prompt": "68",  "answer": "六十八"},
                {"prompt": "100", "answer": "一百"},
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
