import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 14,
    "lesson_code": "HSK1-L14",
    "title": "她买了不少衣服",
    "goal": "The particle 了 for completed actions, 后 as a time marker, and the adverb 都",
    "intro_text": (
        "In lesson fourteen you will learn to express completed actions with 了, "
        "future time with 后, and use the adverb 都. "
        "16 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "东西",  "pinyin": "dōngxi",    "pos": "n.",   "meaning": "thing, item"},
        {"no": 2,  "zh": "一点儿","pinyin": "yīdiǎnr",   "pos": "num.", "meaning": "a little, a bit"},
        {"no": 3,  "zh": "苹果",  "pinyin": "píngguǒ",   "pos": "n.",   "meaning": "apple"},
        {"no": 4,  "zh": "看见",  "pinyin": "kànjiàn",   "pos": "v.",   "meaning": "to see, to catch sight of"},
        {"no": 5,  "zh": "先生",  "pinyin": "xiānsheng", "pos": "n.",   "meaning": "Mr., sir"},
        {"no": 6,  "zh": "开",    "pinyin": "kāi",       "pos": "v.",   "meaning": "to open, to drive (a vehicle)"},
        {"no": 7,  "zh": "车",    "pinyin": "chē",       "pos": "n.",   "meaning": "car, vehicle"},
        {"no": 8,  "zh": "回来",  "pinyin": "huílai",    "pos": "v.",   "meaning": "to come back, to return"},
        {"no": 9,  "zh": "分钟",  "pinyin": "fēnzhōng",  "pos": "n.",   "meaning": "minute (unit of time)"},
        {"no": 10, "zh": "后",    "pinyin": "hòu",       "pos": "n.",   "meaning": "after, later"},
        {"no": 11, "zh": "衣服",  "pinyin": "yīfu",      "pos": "n.",   "meaning": "clothes, clothing"},
        {"no": 12, "zh": "漂亮",  "pinyin": "piàoliang", "pos": "adj.", "meaning": "beautiful, pretty"},
        {"no": 13, "zh": "啊",    "pinyin": "a",         "pos": "part.","meaning": "ah, yes (exclamatory particle)"},
        {"no": 14, "zh": "少",    "pinyin": "shǎo",      "pos": "adj.", "meaning": "few, little"},
        {"no": 15, "zh": "这些",  "pinyin": "zhèxiē",    "pos": "pron.","meaning": "these, these things"},
        {"no": 16, "zh": "都",    "pinyin": "dōu",       "pos": "adv.", "meaning": "all, both"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yotoqxonada — kecha nima qilding",
            "dialogue": [
                {"speaker": "A", "zh": "昨天上午你去哪儿了？",   "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?",     "translation": "Where did you go yesterday morning?"},
                {"speaker": "B", "zh": "我去商店买东西了。",     "pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le.",    "translation": "I went to the store to buy things."},
                {"speaker": "A", "zh": "你买什么了？",           "pinyin": "Nǐ mǎi shénme le?",                 "translation": "What did you buy?"},
                {"speaker": "B", "zh": "我买了一点儿苹果。",     "pinyin": "Wǒ mǎile yīdiǎnr píngguǒ.",        "translation": "I bought a few apples."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Kompaniyada — Zhang janobni ko'rdingizmi",
            "dialogue": [
                {"speaker": "A", "zh": "你看见张先生了吗？",        "pinyin": "Nǐ kànjiàn Zhāng xiānsheng le ma?",      "translation": "Did you see Mr. Zhang?"},
                {"speaker": "B", "zh": "看见了，他去学开车了。",    "pinyin": "Kànjiàn le, tā qù xué kāi chē le.",      "translation": "Yes I did; he went to learn how to drive."},
                {"speaker": "A", "zh": "他什么时候能回来？",        "pinyin": "Tā shénme shíhou néng huílai?",           "translation": "When can he come back?"},
                {"speaker": "B", "zh": "40分钟后回来。",           "pinyin": "Sìshí fēnzhōng hòu huílai.",             "translation": "He will be back in 40 minutes."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Do'kon oldida — kiyimlar",
            "dialogue": [
                {"speaker": "A", "zh": "王方的衣服太漂亮了！",     "pinyin": "Wáng Fāng de yīfu tài piàoliang le!",    "translation": "Wang Fang's clothes are so beautiful!"},
                {"speaker": "B", "zh": "是啊，她买了不少衣服。",   "pinyin": "Shì a, tā mǎile bùshǎo yīfu.",          "translation": "Yes indeed, she bought quite a lot of clothes."},
                {"speaker": "A", "zh": "你买什么了？",             "pinyin": "Nǐ mǎi shénme le?",                     "translation": "What did you buy?"},
                {"speaker": "B", "zh": "我没买，这些都是王方的东西。","pinyin": "Wǒ méi mǎi, zhèxiē dōu shì Wáng Fāng de dōngxi.", "translation": "I didn't buy anything; all of these are Wang Fang's things."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "了 — Harakat tugallangani",
            "explanation": (
                "了(le) at the end of a sentence indicates that an action has occurred or is completed.\n\n"
                "Structure:\n"
                "Subject + Verb + 了 (end of sentence)\n"
                "Subject + Verb + 了 + Number/Adjective + Noun\n\n"
                "Example:\n"
                "我去商店了。— I went to the store.\n"
                "她买了不少衣服。— She bought quite a lot of clothes.\n"
                "我买了一点儿苹果。— I bought a few apples.\n\n"
                "Negation: 没 + Verb (了 is dropped)\n"
                "我没买。— I didn't buy anything.\n"
                "她没去商店。— She didn't go to the store."
            ),
            "examples": [
                {"zh": "我去商店了。",       "pinyin": "Wǒ qù shāngdiàn le.",    "meaning": "I went to the store."},
                {"zh": "她买了不少衣服。",   "pinyin": "Tā mǎile bùshǎo yīfu.", "meaning": "She bought quite a lot of clothes."},
                {"zh": "我没买。",           "pinyin": "Wǒ méi mǎi.",            "meaning": "I didn't buy anything."},
            ]
        },
        {
            "no": 2,
            "title_zh": "名词 后 — 后 vaqt belgisi",
            "explanation": (
                "后(hòu) — indicates a point in time after a certain event.\n\n"
                "40分钟后 — in 40 minutes\n"
                "三天后 — in three days\n"
                "一个星期后 — in one week\n"
                "五点后 — after five o'clock\n\n"
                "Example:\n"
                "40分钟后回来。— He will be back in 40 minutes.\n"
                "三天后我去北京。— I will go to Beijing in three days."
            ),
            "examples": [
                {"zh": "40分钟后回来。",   "pinyin": "Sìshí fēnzhōng hòu huílai.", "meaning": "He will be back in 40 minutes."},
                {"zh": "三天后见。",       "pinyin": "Sān tiān hòu jiàn.",         "meaning": "See you in three days."},
                {"zh": "八点后能来吗？",   "pinyin": "Bā diǎn hòu néng lái ma?",   "meaning": "Can you come after eight o'clock?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "副词 都 — Ravish 都 (hammasi)",
            "explanation": (
                "都(dōu) — means 'all, both, every one'.\n"
                "Important: the items being listed come BEFORE 都.\n\n"
                "Example:\n"
                "这些都是王方的东西。— All of these are Wang Fang's things.\n"
                "我们都是中国人。— We are all Chinese.\n"
                "他们都喜欢喝茶。— They all like drinking tea."
            ),
            "examples": [
                {"zh": "这些都是王方的东西。", "pinyin": "Zhèxiē dōu shì Wáng Fāng de dōngxi.", "meaning": "All of these are Wang Fang's things."},
                {"zh": "我们都是中国人。",     "pinyin": "Wǒmen dōu shì Zhōngguó rén.",         "meaning": "We are all Chinese."},
                {"zh": "他们都喜欢喝茶。",     "pinyin": "Tāmen dōu xǐhuan hē chá.",           "meaning": "They all like drinking tea."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Where did you go yesterday morning?",     "answer": "昨天上午你去哪儿了？",  "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?"},
                {"prompt": "I went to the store to buy things.", "answer": "我去商店买东西了。","pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le."},
                {"prompt": "She bought quite a lot of clothes.",             "answer": "她买了不少衣服。",      "pinyin": "Tā mǎile bùshǎo yīfu."},
                {"prompt": "He will be back in 40 minutes.",          "answer": "40分钟后回来。",        "pinyin": "Sìshí fēnzhōng hòu huílai."},
                {"prompt": "All of these are his things.",       "answer": "这些都是他的东西。",    "pinyin": "Zhèxiē dōu shì tā de dōngxi."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "我去商店买东西___。",       "answer": "了",  "pinyin": "le"},
                {"prompt": "40分钟___回来。",           "answer": "后",  "pinyin": "hòu"},
                {"prompt": "这些___是王方的东西。",     "answer": "都",  "pinyin": "dōu"},
                {"prompt": "我___买，这些不是我的。",   "answer": "没",  "pinyin": "méi"},
            ]
        },
        {
            "no": 3,
            "type": "negative",
            "instruction": "Make the sentence negative (using 没):",
            "items": [
                {"prompt": "她买了不少衣服。",   "answer": "她没买衣服。",     "pinyin": "Tā méi mǎi yīfu."},
                {"prompt": "我去商店了。",       "answer": "我没去商店。",     "pinyin": "Wǒ méi qù shāngdiàn."},
                {"prompt": "他看见张先生了。",   "answer": "他没看见张先生。", "pinyin": "Tā méi kànjiàn Zhāng xiānsheng."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["昨天上午你去哪儿了？", "我去商店买东西了。", "她买了不少衣服。", "40分钟后回来。", "这些都是他的东西。"]},
        {"no": 2, "answers": ["了", "后", "都", "没"]},
        {"no": 3, "answers": ["她没买衣服。", "我没去商店。", "他没看见张先生。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write about yesterday using 了 (4 sentences):",
            "template": "昨天我___了。我买了___。我没___。___后我回家了。",
            "words": ["了", "没", "去", "买", "后", "分钟"],
        },
        {
            "no": 2,
            "instruction": "Answer using 都:",
            "items": [
                {"prompt": "你的朋友都是中国人吗？", "hint": "Yes/no, use 都"},
                {"prompt": "桌子上的东西都是谁的？", "hint": "State whose things they are"},
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
