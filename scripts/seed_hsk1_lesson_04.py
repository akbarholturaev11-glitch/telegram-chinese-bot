import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 4,
    "lesson_code": "HSK1-L04",
    "title": "她是我的汉语老师",
    "goal": "Talk about third persons, express possession with 的, and use 谁/哪 question words",
    "intro_text": (
        "In the fourth lesson you will learn how to talk about third persons (he/she), "
        "express possession using the particle 的, and use the question words 谁/哪. "
        "10 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "她",   "pinyin": "tā",      "pos": "pron.", "meaning": "she, her"},
        {"no": 2,  "zh": "谁",   "pinyin": "shéi",    "pos": "pron.", "meaning": "who"},
        {"no": 3,  "zh": "的",   "pinyin": "de",      "pos": "part.", "meaning": "'s (possessive particle)"},
        {"no": 4,  "zh": "汉语", "pinyin": "Hànyǔ",   "pos": "n.",    "meaning": "Chinese language"},
        {"no": 5,  "zh": "哪",   "pinyin": "nǎ",      "pos": "pron.", "meaning": "which, where from"},
        {"no": 6,  "zh": "国",   "pinyin": "guó",     "pos": "n.",    "meaning": "country, nation"},
        {"no": 7,  "zh": "呢",   "pinyin": "ne",      "pos": "part.", "meaning": "what about? (follow-up question)"},
        {"no": 8,  "zh": "他",   "pinyin": "tā",      "pos": "pron.", "meaning": "he, him"},
        {"no": 9,  "zh": "同学", "pinyin": "tóngxué", "pos": "n.",    "meaning": "classmate"},
        {"no": 10, "zh": "朋友", "pinyin": "péngyou", "pos": "n.",    "meaning": "friend"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Sinfda — o'qituvchi haqida",
            "dialogue": [
                {"speaker": "A", "zh": "她是谁？",              "pinyin": "Tā shì shéi?",                       "translation": "Who is she?"},
                {"speaker": "B", "zh": "她是我的汉语老师，她叫李月。", "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī, tā jiào Lǐ Yuè.", "translation": "She is my Chinese teacher, her name is Li Yue."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Kutubxonada — millat so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是哪国人？",    "pinyin": "Nǐ shì nǎ guó rén?",       "translation": "What country are you from?"},
                {"speaker": "B", "zh": "我是美国人。你呢？","pinyin": "Wǒ shì Měiguó rén. Nǐ ne?", "translation": "I am American. What about you?"},
                {"speaker": "A", "zh": "我是中国人。",    "pinyin": "Wǒ shì Zhōngguó rén.",     "translation": "I am Chinese."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Fotoda — do'st va sinfdosh",
            "dialogue": [
                {"speaker": "A", "zh": "他是谁？",                "pinyin": "Tā shì shéi?",                           "translation": "Who is he?"},
                {"speaker": "B", "zh": "他是我同学。",             "pinyin": "Tā shì wǒ tóngxué.",                    "translation": "He is my classmate."},
                {"speaker": "A", "zh": "她呢？她是你同学吗？",     "pinyin": "Tā ne? Tā shì nǐ tóngxué ma?",          "translation": "What about her? Is she also your classmate?"},
                {"speaker": "B", "zh": "她不是我同学，她是我朋友。","pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou.", "translation": "She is not my classmate, she is my friend."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "结构助词 的 — Egalik yuklamasi",
            "explanation": (
                "的(de) — expresses possession or association.\n"
                "Structure: Noun/Pronoun + 的 + Noun\n\n"
                "Example:\n"
                "我的老师 — my teacher\n"
                "她的朋友 — her friend\n\n"
                "Note: 的 can be omitted before kinship terms and personal nouns:\n"
                "我(的)老师 ✓ — my teacher\n"
                "我(的)朋友 ✓ — my friend"
            ),
            "examples": [
                {"zh": "我的汉语老师",   "pinyin": "wǒ de Hànyǔ lǎoshī", "meaning": "my Chinese teacher"},
                {"zh": "他的同学",       "pinyin": "tā de tóngxué",       "meaning": "his classmate"},
                {"zh": "你的朋友",       "pinyin": "nǐ de péngyou",       "meaning": "your friend"},
            ]
        },
        {
            "no": 2,
            "title_zh": "谁 — Kim so'roq olmoshi",
            "explanation": (
                "谁(shéi) — means 'who?'.\n"
                "It can function as the subject or object in a sentence.\n\n"
                "Example:\n"
                "她是谁？— Who is she?\n"
                "谁是老师？— Who is the teacher?\n"
                "他是谁的朋友？— Whose friend is he?"
            ),
            "examples": [
                {"zh": "她是谁？",       "pinyin": "Tā shì shéi?",        "meaning": "Who is she?"},
                {"zh": "谁是你的老师？", "pinyin": "Shéi shì nǐ de lǎoshī?", "meaning": "Who is your teacher?"},
                {"zh": "他是谁的同学？", "pinyin": "Tā shì shéi de tóngxué?", "meaning": "Whose classmate is he?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "呢 — Qaytarma so'roq yuklamasi",
            "explanation": (
                "呢(ne) — used to ask about the same topic mentioned in the previous sentence.\n"
                "Structure: Statement A... B呢？ (What about B?)\n\n"
                "Example:\n"
                "我是美国人。你呢？\n"
                "I am American. What about you?\n\n"
                "她叫李月。他呢？\n"
                "Her name is Li Yue. What about him?"
            ),
            "examples": [
                {"zh": "我是学生。你呢？",  "pinyin": "Wǒ shì xuésheng. Nǐ ne?", "meaning": "I am a student. What about you?"},
                {"zh": "她是中国人。他呢？","pinyin": "Tā shì Zhōngguó rén. Tā ne?","meaning": "She is Chinese. What about him?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Who is she?",                              "answer": "她是谁？",                  "pinyin": "Tā shì shéi?"},
                {"prompt": "She is my Chinese teacher.",               "answer": "她是我的汉语老师。",         "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī."},
                {"prompt": "What country are you from?",              "answer": "你是哪国人？",               "pinyin": "Nǐ shì nǎ guó rén?"},
                {"prompt": "I am American. What about you?",          "answer": "我是美国人。你呢？",         "pinyin": "Wǒ shì Měiguó rén. Nǐ ne?"},
                {"prompt": "He is not my classmate, he is my friend.","answer": "他不是我同学，他是我朋友。", "pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "她是我___汉语老师。",            "answer": "的",   "pinyin": "de"},
                {"prompt": "A: 他是___？  B: 他是我同学。", "answer": "谁",   "pinyin": "shéi"},
                {"prompt": "我是中国人。你___？",             "answer": "呢",   "pinyin": "ne"},
                {"prompt": "你是___国人？",                   "answer": "哪",   "pinyin": "nǎ"},
            ]
        },
        {
            "no": 3,
            "type": "make_sentence",
            "instruction": "Make a sentence from the given words:",
            "items": [
                {"words": ["她", "是", "我", "的", "朋友"], "answer": "她是我的朋友。",       "pinyin": "Tā shì wǒ de péngyou."},
                {"words": ["他", "哪", "是", "国", "人"],   "answer": "他是哪国人？",         "pinyin": "Tā shì nǎ guó rén?"},
                {"words": ["谁", "你", "老师", "是", "的"], "answer": "谁是你的老师？",       "pinyin": "Shéi shì nǐ de lǎoshī?"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["她是谁？", "她是我的汉语老师。", "你是哪国人？", "我是美国人。你呢？", "他不是我同学，他是我朋友。"]},
        {"no": 2, "answers": ["的", "谁", "呢", "哪"]},
        {"no": 3, "answers": ["她是我的朋友。", "他是哪国人？", "谁是你的老师？"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 4 sentences about a friend:",
            "template": "他/她叫___。他/她是___人。他/她是我的___。他/她是不是___？",
            "words": ["的", "同学", "朋友", "老师", "汉语老师"],
        },
        {
            "no": 2,
            "instruction": "Answer the following questions:",
            "items": [
                {"prompt": "你的汉语老师是哪国人？",    "hint": "What country is your Chinese teacher from?"},
                {"prompt": "你的朋友叫什么名字？",       "hint": "What is your friend's name?"},
                {"prompt": "他/她是你的同学吗？",        "hint": "Is he/she your classmate?"},
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
