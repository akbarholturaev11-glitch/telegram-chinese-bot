import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 7,
    "lesson_code": "HSK1-L07",
    "title": "今天几号",
    "goal": "Learning dates, days of the week, and serial verb sentences",
    "intro_text": (
        "In the seventh lesson you will learn to say today's date, days of the week, "
        "and the 去+place+action construction. "
        "12 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "请",   "pinyin": "qǐng",    "pos": "v.",   "meaning": "please, may I ask"},
        {"no": 2,  "zh": "问",   "pinyin": "wèn",     "pos": "v.",   "meaning": "to ask"},
        {"no": 3,  "zh": "今天", "pinyin": "jīntiān", "pos": "n.",   "meaning": "today"},
        {"no": 4,  "zh": "号",   "pinyin": "hào",     "pos": "n.",   "meaning": "date (day of the month)"},
        {"no": 5,  "zh": "月",   "pinyin": "yuè",     "pos": "n.",   "meaning": "month (January, February, etc.)"},
        {"no": 6,  "zh": "星期", "pinyin": "xīngqī",  "pos": "n.",   "meaning": "week, day of the week"},
        {"no": 7,  "zh": "昨天", "pinyin": "zuótiān", "pos": "n.",   "meaning": "yesterday"},
        {"no": 8,  "zh": "明天", "pinyin": "míngtiān","pos": "n.",   "meaning": "tomorrow"},
        {"no": 9,  "zh": "去",   "pinyin": "qù",      "pos": "v.",   "meaning": "to go"},
        {"no": 10, "zh": "学校", "pinyin": "xuéxiào", "pos": "n.",   "meaning": "school"},
        {"no": 11, "zh": "看",   "pinyin": "kàn",     "pos": "v.",   "meaning": "to look, to watch, to read"},
        {"no": 12, "zh": "书",   "pinyin": "shū",     "pos": "n.",   "meaning": "book"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Bankda — bugungi sana",
            "dialogue": [
                {"speaker": "A", "zh": "请问，今天几号？",  "pinyin": "Qǐngwèn, jīntiān jǐ hào?",  "translation": "Excuse me, what is today's date?"},
                {"speaker": "B", "zh": "今天9月1号。",     "pinyin": "Jīntiān jiǔ yuè yī hào.",   "translation": "Today is September 1st."},
                {"speaker": "A", "zh": "今天星期几？",      "pinyin": "Jīntiān xīngqī jǐ?",        "translation": "What day of the week is today?"},
                {"speaker": "B", "zh": "星期三。",          "pinyin": "Xīngqī sān.",                "translation": "Wednesday."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Taqvimga qarab — kecha va ertaga",
            "dialogue": [
                {"speaker": "A", "zh": "昨天是几月几号？",         "pinyin": "Zuótiān shì jǐ yuè jǐ hào?",          "translation": "What month and day was yesterday?"},
                {"speaker": "B", "zh": "昨天是8月31号，星期二。",  "pinyin": "Zuótiān shì bā yuè sānshíyī hào, xīngqī èr.", "translation": "Yesterday was August 31st, Tuesday."},
                {"speaker": "A", "zh": "明天呢？",                 "pinyin": "Míngtiān ne?",                         "translation": "And tomorrow?"},
                {"speaker": "B", "zh": "明天是9月2号，星期四。",   "pinyin": "Míngtiān shì jiǔ yuè èr hào, xīngqī sì.", "translation": "Tomorrow is September 2nd, Thursday."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Qahvaxonada — ertangi reja",
            "dialogue": [
                {"speaker": "A", "zh": "明天星期六，你去学校吗？",  "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?", "translation": "Tomorrow is Saturday — are you going to school?"},
                {"speaker": "B", "zh": "我去学校。",               "pinyin": "Wǒ qù xuéxiào.",                        "translation": "I am going to school."},
                {"speaker": "A", "zh": "你去学校做什么？",          "pinyin": "Nǐ qù xuéxiào zuò shénme?",            "translation": "What are you going to school to do?"},
                {"speaker": "B", "zh": "我去学校看书。",            "pinyin": "Wǒ qù xuéxiào kàn shū.",               "translation": "I am going to school to read."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "日期的表达 — Sana ifodalash",
            "explanation": (
                "In Chinese, dates are expressed from largest to smallest unit:\n"
                "Year → Month → Day → Day of the week\n\n"
                "Month: 一月(January) ~ 十二月(December)\n"
                "Day: 1号(1st) ~ 31号(31st)\n\n"
                "Days of the week:\n"
                "星期一 Monday\n"
                "星期二 Tuesday\n"
                "星期三 Wednesday\n"
                "星期四 Thursday\n"
                "星期五 Friday\n"
                "星期六 Saturday\n"
                "星期日/星期天 Sunday\n\n"
                "Example: 9月1号，星期三 — September 1st, Wednesday"
            ),
            "examples": [
                {"zh": "今天9月1号，星期三。",  "pinyin": "Jīntiān jiǔ yuè yī hào, xīngqī sān.", "meaning": "Today is September 1st, Wednesday."},
                {"zh": "明天星期六。",          "pinyin": "Míngtiān xīngqī liù.",                "meaning": "Tomorrow is Saturday."},
                {"zh": "昨天8月31号。",         "pinyin": "Zuótiān bā yuè sānshíyī hào.",        "meaning": "Yesterday was August 31st."},
            ]
        },
        {
            "no": 2,
            "title_zh": "名词谓语句 — Ot kesimli gap",
            "explanation": (
                "A noun or number can serve as the predicate (是 is not required).\n"
                "Often used to express age, dates, and time.\n\n"
                "Example:\n"
                "今天9月1号。— Today is September 1st. (9月1号 is the noun predicate)\n"
                "明天星期三。— Tomorrow is Wednesday.\n"
                "我的汉语老师33岁。— My Chinese teacher is 33 years old."
            ),
            "examples": [
                {"zh": "今天9月1号。",   "pinyin": "Jīntiān jiǔ yuè yī hào.",  "meaning": "Today is September 1st."},
                {"zh": "明天星期三。",   "pinyin": "Míngtiān xīngqī sān.",     "meaning": "Tomorrow is Wednesday."},
                {"zh": "她今年二十岁。", "pinyin": "Tā jīnnián èrshí suì.",    "meaning": "She is twenty years old this year."},
            ]
        },
        {
            "no": 3,
            "title_zh": "连动句 — 去+joy+nima qilish",
            "explanation": (
                "Serial verb sentence: the first action expresses the purpose of the second.\n"
                "Structure: Subject + 去 + Place + Verb + Object\n\n"
                "Example:\n"
                "我去学校看书。— I go to school to read.\n"
                "我去中国学习汉语。— I go to China to study Chinese.\n\n"
                "Question: 你去哪儿做什么？— Where are you going and what will you do?"
            ),
            "examples": [
                {"zh": "我去学校看书。",     "pinyin": "Wǒ qù xuéxiào kàn shū.",        "meaning": "I go to school to read."},
                {"zh": "她去学校学汉语。",   "pinyin": "Tā qù xuéxiào xué Hànyǔ.",     "meaning": "She goes to school to study Chinese."},
                {"zh": "你去哪儿做什么？",   "pinyin": "Nǐ qù nǎr zuò shénme?",        "meaning": "Where are you going and what will you do?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "date_writing",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "March 3rd, Monday",              "answer": "3月3号，星期一",    "pinyin": "sān yuè sān hào, xīngqī yī"},
                {"prompt": "May 15th, Friday",               "answer": "5月15号，星期五",   "pinyin": "wǔ yuè shíwǔ hào, xīngqī wǔ"},
                {"prompt": "December 31st, Sunday",          "answer": "12月31号，星期日",  "pinyin": "shí'èr yuè sānshíyī hào, xīngqīrì"},
                {"prompt": "What is today's date?",          "answer": "今天几号？",        "pinyin": "Jīntiān jǐ hào?"},
                {"prompt": "What day of the week is today?", "answer": "今天星期几？",      "pinyin": "Jīntiān xīngqī jǐ?"},
            ]
        },
        {
            "no": 2,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Excuse me, what is today's date?",              "answer": "请问，今天几号？",       "pinyin": "Qǐngwèn, jīntiān jǐ hào?"},
                {"prompt": "Tomorrow is Saturday — are you going to school?","answer": "明天星期六，你去学校吗？", "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?"},
                {"prompt": "I am going to school to read.",                  "answer": "我去学校看书。",         "pinyin": "Wǒ qù xuéxiào kàn shū."},
            ]
        },
        {
            "no": 3,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "今天___月___号，___期___。",        "answer": "enter today's date", "pinyin": "write today's date"},
                {"prompt": "我___学校___书。",                  "answer": "去/看",              "pinyin": "qù/kàn"},
                {"prompt": "___天是9月2号，星期四。",           "answer": "明",                 "pinyin": "míng"},
                {"prompt": "请___，今天星期几？",               "answer": "问",                 "pinyin": "wèn"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["3月3号，星期一", "5月15号，星期五", "12月31号，星期日", "今天几号？", "今天星期几？"]},
        {"no": 2, "answers": ["请问，今天几号？", "明天星期六，你去学校吗？", "我去学校看书。"]},
        {"no": 3, "answers": ["today's date", "去/看", "明", "问"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write today's, yesterday's, and tomorrow's dates:",
            "template": "昨天是___月___号，星期___。今天是___月___号，星期___。明天是___月___号，星期___。",
        },
        {
            "no": 2,
            "instruction": "Write your plans for tomorrow (using 去+place+action):",
            "example": "明天我去___。",
            "words": ["去", "学校", "看书", "说汉语", "做中国菜"],
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
