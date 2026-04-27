import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 15,
    "lesson_code": "HSK1-L15",
    "title": "我是坐飞机来的",
    "goal": "The 是……的 construction — emphasising time, place, and manner",
    "intro_text": (
        "In lesson fifteen — the final lesson — you will learn to use the 是……的 construction "
        "to emphasise when, where, and how something was done. "
        "9 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "认识",  "pinyin": "rènshi",   "pos": "v.",   "meaning": "to know, to meet, to recognise"},
        {"no": 2, "zh": "年",    "pinyin": "nián",     "pos": "n.",   "meaning": "year"},
        {"no": 3, "zh": "大学",  "pinyin": "dàxué",    "pos": "n.",   "meaning": "university, college"},
        {"no": 4, "zh": "饭店",  "pinyin": "fàndiàn",  "pos": "n.",   "meaning": "restaurant, hotel"},
        {"no": 5, "zh": "出租车","pinyin": "chūzūchē", "pos": "n.",   "meaning": "taxi"},
        {"no": 6, "zh": "一起",  "pinyin": "yīqǐ",     "pos": "adv.", "meaning": "together"},
        {"no": 7, "zh": "高兴",  "pinyin": "gāoxìng",  "pos": "adj.", "meaning": "happy, glad"},
        {"no": 8, "zh": "听",    "pinyin": "tīng",     "pos": "v.",   "meaning": "to listen, to hear"},
        {"no": 9, "zh": "飞机",  "pinyin": "fēijī",    "pos": "n.",   "meaning": "airplane"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Dasturxon yonida — qachon va qayerda tanishdingiz",
            "dialogue": [
                {"speaker": "A", "zh": "你和李小姐是什么时候认识的？",    "pinyin": "Nǐ hé Lǐ xiǎojiě shì shénme shíhou rènshi de?",    "translation": "When did you meet Miss Li?"},
                {"speaker": "B", "zh": "我们是2011年9月认识的。",        "pinyin": "Wǒmen shì èr líng yī yī nián jiǔ yuè rènshi de.",  "translation": "We met in September 2011."},
                {"speaker": "A", "zh": "你们在哪儿认识的？",             "pinyin": "Nǐmen zài nǎr rènshi de?",                         "translation": "Where did you two meet?"},
                {"speaker": "B", "zh": "我们是在学校认识的，她是我大学同学。","pinyin": "Wǒmen shì zài xuéxiào rènshi de, tā shì wǒ dàxué tóngxué.", "translation": "We met at school; she is my university classmate."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Mehmonxona oldida — qanday keldingiz",
            "dialogue": [
                {"speaker": "A", "zh": "你们是怎么来饭店的？",          "pinyin": "Nǐmen shì zěnme lái fàndiàn de?",                "translation": "How did you get to the restaurant?"},
                {"speaker": "B", "zh": "我们是坐出租车来的。",          "pinyin": "Wǒmen shì zuò chūzūchē lái de.",               "translation": "We came by taxi."},
                {"speaker": "A", "zh": "李先生呢？",                    "pinyin": "Lǐ xiānsheng ne?",                             "translation": "What about Mr. Li?"},
                {"speaker": "B", "zh": "他是和朋友一起开车来的。",      "pinyin": "Tā shì hé péngyou yīqǐ kāi chē lái de.",       "translation": "He came by car together with a friend."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kompaniyada — samolyot bilan kelding",
            "dialogue": [
                {"speaker": "A", "zh": "很高兴认识您！李小姐。",          "pinyin": "Hěn gāoxìng rènshi nín! Lǐ xiǎojiě.",          "translation": "It's a pleasure to meet you, Miss Li!"},
                {"speaker": "B", "zh": "认识你我也很高兴！",             "pinyin": "Rènshi nǐ wǒ yě hěn gāoxìng!",                "translation": "It's a pleasure to meet you too!"},
                {"speaker": "A", "zh": "听张先生说，您是坐飞机来北京的？","pinyin": "Tīng Zhāng xiānsheng shuō, nín shì zuò fēijī lái Běijīng de?", "translation": "Mr. Zhang mentioned that you came to Beijing by plane?"},
                {"speaker": "B", "zh": "是的。",                        "pinyin": "Shì de.",                                      "translation": "That's right."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "是……的 — Vaqt, joy va usulni ta'kidlash",
            "explanation": (
                "The 是……的 construction is used to emphasise the time, "
                "place, or manner of an action that has already occurred.\n\n"
                "Structure:\n"
                "Subject + 是 + [Time/Place/Manner] + Verb + 的\n\n"
                "Emphasising time:\n"
                "我们是2011年认识的。— We met in 2011.\n\n"
                "Emphasising place:\n"
                "我们是在学校认识的。— We met at school.\n\n"
                "Emphasising manner:\n"
                "我是坐飞机来的。— I came by plane.\n\n"
                "Negation: 不是……的\n"
                "我不是坐出租车来的。— I didn't come by taxi."
            ),
            "examples": [
                {"zh": "我们是2011年认识的。",   "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de.",   "meaning": "We met in 2011."},
                {"zh": "我是坐飞机来的。",        "pinyin": "Wǒ shì zuò fēijī lái de.",                 "meaning": "I came by plane."},
                {"zh": "她是在北京买的。",        "pinyin": "Tā shì zài Běijīng mǎi de.",               "meaning": "She bought it in Beijing."},
                {"zh": "我们不是坐出租车来的。",  "pinyin": "Wǒmen bú shì zuò chūzūchē lái de.",        "meaning": "We didn't come by taxi."},
            ]
        },
        {
            "no": 2,
            "title_zh": "日期的表达(2) — To'liq sana ifodalash",
            "explanation": (
                "In Chinese, a full date is expressed from largest to smallest unit:\n"
                "Year + Month + Day + Day of the week\n\n"
                "Reading years: each digit is read separately\n"
                "2011 → 二零一一年 (èr líng yī yī nián)\n"
                "2024 → 二零二四年 (èr líng èr sì nián)\n\n"
                "Full example:\n"
                "2011年9月10号，星期三\n"
                "Year 2011, September, 10th, Wednesday"
            ),
            "examples": [
                {"zh": "2011年9月认识的",     "pinyin": "èr líng yī yī nián jiǔ yuè rènshi de", "meaning": "met in September 2011"},
                {"zh": "今天是2024年4月26号。","pinyin": "Jīntiān shì èr líng èr sì nián sì yuè èrshíliù hào.", "meaning": "Today is April 26, 2024."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese (using 是……的):",
            "items": [
                {"prompt": "We met in 2011.",          "answer": "我们是2011年认识的。",       "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de."},
                {"prompt": "I came by plane.",              "answer": "我是坐飞机来的。",           "pinyin": "Wǒ shì zuò fēijī lái de."},
                {"prompt": "How did you get to the restaurant?",  "answer": "你是怎么来饭店的？",         "pinyin": "Nǐ shì zěnme lái fàndiàn de?"},
                {"prompt": "We came by taxi.",             "answer": "我们是坐出租车来的。",       "pinyin": "Wǒmen shì zuò chūzūchē lái de."},
                {"prompt": "He came together with a friend.",         "answer": "他是和朋友一起来的。",       "pinyin": "Tā shì hé péngyou yīqǐ lái de."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "你们___什么时候认识的？",    "answer": "是",   "pinyin": "shì"},
                {"prompt": "我是坐飞机来___。",          "answer": "的",   "pinyin": "de"},
                {"prompt": "他们是___学校认识的。",      "answer": "在",   "pinyin": "zài"},
                {"prompt": "我不___坐出租车来的。",      "answer": "是",   "pinyin": "shì"},
            ]
        },
        {
            "no": 3,
            "type": "emphasis",
            "instruction": "Add emphasis using 是……的:",
            "items": [
                {"prompt": "我坐飞机来。(emphasise manner)",      "answer": "我是坐飞机来的。",         "pinyin": "Wǒ shì zuò fēijī lái de."},
                {"prompt": "他们在北京认识。(emphasise place)",   "answer": "他们是在北京认识的。",     "pinyin": "Tāmen shì zài Běijīng rènshi de."},
                {"prompt": "我2011年来中国。(emphasise time)",  "answer": "我是2011年来中国的。",     "pinyin": "Wǒ shì èr líng yī yī nián lái Zhōngguó de."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["我们是2011年认识的。", "我是坐飞机来的。", "你是怎么来饭店的？", "我们是坐出租车来的。", "他是和朋友一起来的。"]},
        {"no": 2, "answers": ["是", "的", "在", "是"]},
        {"no": 3, "answers": ["我是坐飞机来的。", "他们是在北京认识的。", "我是2011年来中国的。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 4 sentences about yourself using 是……的:",
            "template": "我是___年___的。我是在___认识___的。我是坐___来___的。",
            "words": ["是", "的", "在", "年", "坐", "飞机", "出租车", "认识"],
        },
        {
            "no": 2,
            "instruction": "Ask your friend questions using 是……的:",
            "items": [
                {"prompt": "When did you two meet?",     "example": "你们是什么时候认识的？"},
                {"prompt": "Where did you two meet?",    "example": "你们是在哪儿认识的？"},
                {"prompt": "How did he get here?",             "example": "他是怎么来的？"},
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
