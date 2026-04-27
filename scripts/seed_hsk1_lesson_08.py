import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 8,
    "lesson_code": "HSK1-L08",
    "title": "我想喝茶",
    "goal": "Expressing wishes, asking prices, and learning measure words",
    "intro_text": (
        "In the eighth lesson you will learn to express wishes using the modal verb 想, "
        "ask prices (多少钱?), and use the measure words 个/口. "
        "15 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "想",   "pinyin": "xiǎng",    "pos": "mod.", "meaning": "to want, to wish"},
        {"no": 2,  "zh": "喝",   "pinyin": "hē",       "pos": "v.",   "meaning": "to drink"},
        {"no": 3,  "zh": "茶",   "pinyin": "chá",      "pos": "n.",   "meaning": "tea"},
        {"no": 4,  "zh": "吃",   "pinyin": "chī",      "pos": "v.",   "meaning": "to eat"},
        {"no": 5,  "zh": "米饭", "pinyin": "mǐfàn",    "pos": "n.",   "meaning": "rice, cooked rice"},
        {"no": 6,  "zh": "下午", "pinyin": "xiàwǔ",    "pos": "n.",   "meaning": "afternoon"},
        {"no": 7,  "zh": "商店", "pinyin": "shāngdiàn","pos": "n.",   "meaning": "shop, store"},
        {"no": 8,  "zh": "买",   "pinyin": "mǎi",      "pos": "v.",   "meaning": "to buy"},
        {"no": 9,  "zh": "个",   "pinyin": "gè",       "pos": "m.",   "meaning": "general measure word (piece/unit)"},
        {"no": 10, "zh": "杯子", "pinyin": "bēizi",    "pos": "n.",   "meaning": "cup, glass"},
        {"no": 11, "zh": "这",   "pinyin": "zhè",      "pos": "pron.","meaning": "this (demonstrative pronoun)"},
        {"no": 12, "zh": "多少", "pinyin": "duōshao",  "pos": "pron.","meaning": "how much, how many (10+)"},
        {"no": 13, "zh": "钱",   "pinyin": "qián",     "pos": "n.",   "meaning": "money"},
        {"no": 14, "zh": "块",   "pinyin": "kuài",     "pos": "m.",   "meaning": "yuan (colloquial)"},
        {"no": 15, "zh": "那",   "pinyin": "nà",       "pos": "pron.","meaning": "that (demonstrative pronoun)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Restoranда — nima ichish/yeyish",
            "dialogue": [
                {"speaker": "A", "zh": "你想喝什么？",  "pinyin": "Nǐ xiǎng hē shénme?",  "translation": "What would you like to drink?"},
                {"speaker": "B", "zh": "我想喝茶。",    "pinyin": "Wǒ xiǎng hē chá.",     "translation": "I would like to drink tea."},
                {"speaker": "A", "zh": "你想吃什么？",  "pinyin": "Nǐ xiǎng chī shénme?", "translation": "What would you like to eat?"},
                {"speaker": "B", "zh": "我想吃米饭。",  "pinyin": "Wǒ xiǎng chī mǐfàn.",  "translation": "I would like to eat rice."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Mehmonxonada — tushdan keyingi reja",
            "dialogue": [
                {"speaker": "A", "zh": "下午你想做什么？",   "pinyin": "Xiàwǔ nǐ xiǎng zuò shénme?",   "translation": "What do you want to do this afternoon?"},
                {"speaker": "B", "zh": "下午我想去商店。",   "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn.", "translation": "I want to go to the store this afternoon."},
                {"speaker": "A", "zh": "你想买什么？",       "pinyin": "Nǐ xiǎng mǎi shénme?",         "translation": "What do you want to buy?"},
                {"speaker": "B", "zh": "我想买一个杯子。",   "pinyin": "Wǒ xiǎng mǎi yī gè bēizi.",    "translation": "I want to buy one cup."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Do'konda — narx so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你好！这个杯子多少钱？",  "pinyin": "Nǐ hǎo! Zhège bēizi duōshao qián?", "translation": "Hello! How much is this cup?"},
                {"speaker": "B", "zh": "28块。",                  "pinyin": "Èrshíbā kuài.",                     "translation": "28 yuan."},
                {"speaker": "A", "zh": "那个杯子多少钱？",        "pinyin": "Nàge bēizi duōshao qián?",          "translation": "How much is that cup?"},
                {"speaker": "B", "zh": "那个杯子18块钱。",        "pinyin": "Nàge bēizi shíbā kuài qián.",       "translation": "That cup is 18 yuan."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "能愿动词 想 — Modal fe'l 想",
            "explanation": (
                "想(xiǎng) — expresses a wish or plan.\n"
                "Structure: Subject + 想 + Verb + Object\n\n"
                "Affirmative: 我想喝茶。— I want to drink tea.\n"
                "Question: 你想做什么？— What do you want to do?\n\n"
                "想 vs 会:\n"
                "我想说汉语。— I want to speak Chinese (desire).\n"
                "我会说汉语。— I can speak Chinese (ability)."
            ),
            "examples": [
                {"zh": "我想喝茶。",         "pinyin": "Wǒ xiǎng hē chá.",           "meaning": "I want to drink tea."},
                {"zh": "她想去学校看书。",   "pinyin": "Tā xiǎng qù xuéxiào kàn shū.", "meaning": "She wants to go to school to read."},
                {"zh": "你想买什么？",       "pinyin": "Nǐ xiǎng mǎi shénme?",       "meaning": "What do you want to buy?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "多少 — Qancha so'rog'i (10+)",
            "explanation": (
                "多少(duōshao) — question word for numbers greater than 10.\n"
                "Note: 几(jǐ) is for numbers up to 10; 多少(duōshao) is for numbers above 10.\n\n"
                "Asking price: ……多少钱？\n"
                "这个杯子多少钱？— How much is this cup?\n\n"
                "Asking quantity:\n"
                "你们学校有多少学生？— How many students are at your school?\n"
                "你有多少钱？— How much money do you have?"
            ),
            "examples": [
                {"zh": "这个杯子多少钱？",   "pinyin": "Zhège bēizi duōshao qián?",    "meaning": "How much is this cup?"},
                {"zh": "你家有多少口人？",   "pinyin": "Nǐ jiā yǒu duōshao kǒu rén?", "meaning": "How many people are in your family?"},
                {"zh": "一个苹果多少钱？",   "pinyin": "Yī gè píngguǒ duōshao qián?", "meaning": "How much is one apple?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "量词 个/口 — O'lchov so'zlar",
            "explanation": (
                "In Chinese a measure word is required between a number and a noun.\n\n"
                "个(gè) — the most general measure word:\n"
                "一个杯子 — one cup\n"
                "三个学生 — three students\n"
                "两个老师 — two teachers\n\n"
                "口(kǒu) — used for family members:\n"
                "三口人 — a family of three\n"
                "六口人 — a family of six"
            ),
            "examples": [
                {"zh": "一个杯子",   "pinyin": "yī gè bēizi",    "meaning": "one cup"},
                {"zh": "五个学生",   "pinyin": "wǔ gè xuésheng", "meaning": "five students"},
                {"zh": "三口人",     "pinyin": "sān kǒu rén",    "meaning": "a family of three"},
            ]
        },
        {
            "no": 4,
            "title_zh": "钱数的表达 — Pul miqdori",
            "explanation": (
                "Chinese currency: 人民币 (Renminbi, RMB)\n"
                "Formal: 元(yuán)\n"
                "Colloquial: 块(kuài)\n\n"
                "Example:\n"
                "28块 = 28元 — 28 yuan\n"
                "18块钱 — 18 yuan (spoken form)\n\n"
                "这个杯子多少钱？— How much is this cup?\n"
                "28块。— 28 yuan."
            ),
            "examples": [
                {"zh": "这个多少钱？",  "pinyin": "Zhège duōshao qián?", "meaning": "How much is this?"},
                {"zh": "28块钱。",     "pinyin": "Èrshíbā kuài qián.",  "meaning": "28 yuan."},
                {"zh": "一百块。",     "pinyin": "Yìbǎi kuài.",         "meaning": "100 yuan."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "What would you like to drink?",              "answer": "你想喝什么？",      "pinyin": "Nǐ xiǎng hē shénme?"},
                {"prompt": "I would like to drink tea.",                  "answer": "我想喝茶。",        "pinyin": "Wǒ xiǎng hē chá."},
                {"prompt": "How much is this cup?",                       "answer": "这个杯子多少钱？",  "pinyin": "Zhège bēizi duōshao qián?"},
                {"prompt": "28 yuan.",                                    "answer": "28块钱。",          "pinyin": "Èrshíbā kuài qián."},
                {"prompt": "I want to go to the store this afternoon.",   "answer": "下午我想去商店。",  "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "你___喝什么？",              "answer": "想",    "pinyin": "xiǎng"},
                {"prompt": "这___杯子多少钱？",          "answer": "个",    "pinyin": "gè"},
                {"prompt": "___个杯子18块___。",         "answer": "那/钱", "pinyin": "nà/qián"},
                {"prompt": "我想买___个杯子。",          "answer": "一",    "pinyin": "yī"},
            ]
        },
        {
            "no": 3,
            "type": "price_dialogue",
            "instruction": "Ask and answer about prices:",
            "items": [
                {"prompt": "苹果(apple) — 5块/个",  "question": "这个苹果多少钱？", "answer": "五块钱。"},
                {"prompt": "书(book) — 35块",       "question": "这本书多少钱？",   "answer": "三十五块钱。"},
                {"prompt": "茶(tea) — 18块",        "question": "这个茶多少钱？",   "answer": "十八块钱。"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你想喝什么？", "我想喝茶。", "这个杯子多少钱？", "28块钱。", "下午我想去商店。"]},
        {"no": 2, "answers": ["想", "个", "那/钱", "一"]},
        {"no": 3, "answers": ["五块钱。", "三十五块钱。", "十八块钱。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write your plans for today (using 想, 3–4 sentences):",
            "template": "今天下午我想___。我想___。我想买___。",
            "words": ["想", "喝", "吃", "去", "买", "茶", "米饭", "杯子"],
        },
        {
            "no": 2,
            "instruction": "Write a shop dialogue asking about prices (4 lines):",
            "example": "A: 你好！___多少钱？\nB: ___块。\nA: ___多少钱？\nB: ___块钱。",
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
