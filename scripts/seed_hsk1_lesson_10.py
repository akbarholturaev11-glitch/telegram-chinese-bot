import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 10,
    "lesson_code": "HSK1-L10",
    "title": "我能坐这儿吗",
    "goal": "Expressing location, 有-sentences, modal verb 能, and conjunction 和",
    "intro_text": (
        "In the tenth lesson you will learn to say where things are, "
        "express existence with 有, use the modal verb 能, and the conjunction 和. "
        "12 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "桌子", "pinyin": "zhuōzi",   "pos": "n.",   "meaning": "table, desk"},
        {"no": 2,  "zh": "上",   "pinyin": "shàng",    "pos": "n.",   "meaning": "on top of, above"},
        {"no": 3,  "zh": "电脑", "pinyin": "diànnǎo",  "pos": "n.",   "meaning": "computer"},
        {"no": 4,  "zh": "和",   "pinyin": "hé",       "pos": "conj.","meaning": "and, with"},
        {"no": 5,  "zh": "本",   "pinyin": "běn",      "pos": "m.",   "meaning": "measure word for books"},
        {"no": 6,  "zh": "里",   "pinyin": "lǐ",       "pos": "n.",   "meaning": "inside, within"},
        {"no": 7,  "zh": "前面", "pinyin": "qiánmiàn", "pos": "n.",   "meaning": "front, in front of"},
        {"no": 8,  "zh": "后面", "pinyin": "hòumiàn",  "pos": "n.",   "meaning": "back, behind"},
        {"no": 9,  "zh": "这儿", "pinyin": "zhèr",     "pos": "pron.","meaning": "here"},
        {"no": 10, "zh": "没有", "pinyin": "méiyǒu",   "pos": "adv.", "meaning": "there is not, does not have"},
        {"no": 11, "zh": "能",   "pinyin": "néng",     "pos": "mod.", "meaning": "can, may (ability/permission)"},
        {"no": 12, "zh": "坐",   "pinyin": "zuò",      "pos": "v.",   "meaning": "to sit"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Ofisda — stol ustida nima bor",
            "dialogue": [
                {"speaker": "A", "zh": "桌子上有什么？",           "pinyin": "Zhuōzi shàng yǒu shénme?",          "translation": "What is on the table?"},
                {"speaker": "B", "zh": "桌子上有一个电脑和一本书。", "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo hé yī běn shū.", "translation": "There is a computer and a book on the table."},
                {"speaker": "A", "zh": "杯子在哪儿？",             "pinyin": "Bēizi zài nǎr?",                    "translation": "Where is the cup?"},
                {"speaker": "B", "zh": "杯子在桌子里。",           "pinyin": "Bēizi zài zhuōzi lǐ.",             "translation": "The cup is inside the desk."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sport zalda — oldida va orqasida kim",
            "dialogue": [
                {"speaker": "A", "zh": "前面那个人叫什么名字？",         "pinyin": "Qiánmiàn nàge rén jiào shénme míngzi?",     "translation": "What is the name of the person in front?"},
                {"speaker": "B", "zh": "她叫王方，在医院工作。",         "pinyin": "Tā jiào Wáng Fāng, zài yīyuàn gōngzuò.",   "translation": "Her name is Wang Fang — she works at a hospital."},
                {"speaker": "A", "zh": "后面那个人呢？他叫什么名字？",   "pinyin": "Hòumiàn nàge rén ne? Tā jiào shénme míngzi?", "translation": "And the person behind? What is his name?"},
                {"speaker": "B", "zh": "他叫谢朋，在商店工作。",         "pinyin": "Tā jiào Xiè Péng, zài shāngdiàn gōngzuò.", "translation": "His name is Xie Peng — he works at a store."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kutubxonada — o'tirish so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "这儿有人吗？",   "pinyin": "Zhèr yǒu rén ma?",   "translation": "Is anyone sitting here?"},
                {"speaker": "B", "zh": "没有。",         "pinyin": "Méiyǒu.",             "translation": "No."},
                {"speaker": "A", "zh": "我能坐这儿吗？", "pinyin": "Wǒ néng zuò zhèr ma?","translation": "May I sit here?"},
                {"speaker": "B", "zh": "请坐。",         "pinyin": "Qǐng zuò.",           "translation": "Please, go ahead."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "有字句 — 有 gapi (mavjudlik)",
            "explanation": (
                "有(yǒu) — indicates that something/someone exists at a certain place.\n"
                "Structure: Place + 有 + Thing/Person\n\n"
                "Example:\n"
                "桌子上有一个电脑。— There is a computer on the table.\n"
                "学校里有一个商店。— There is a shop inside the school.\n\n"
                "Negative: 没有 (méiyǒu)\n"
                "椅子下面没有小狗。— There is no dog under the chair.\n"
                "这儿有人吗？ — 没有。— Is anyone here? — No."
            ),
            "examples": [
                {"zh": "桌子上有一个电脑。",   "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo.",  "meaning": "There is a computer on the table."},
                {"zh": "学校里没有商店。",     "pinyin": "Xuéxiào lǐ méiyǒu shāngdiàn.",     "meaning": "There is no shop in the school."},
                {"zh": "这儿有人吗？",         "pinyin": "Zhèr yǒu rén ma?",                 "meaning": "Is anyone here?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "连词 和 — Bog'lovchi 和",
            "explanation": (
                "和(hé) — connects two nouns or pronouns ('and', 'with').\n"
                "Structure: Noun1 + 和 + Noun2\n\n"
                "Example:\n"
                "一个电脑和一本书 — a computer and a book\n"
                "爸爸和妈妈 — father and mother\n"
                "我有一个中国朋友和一个美国朋友。\n\n"
                "Note: 和 only connects nouns and pronouns —\n"
                "it cannot connect verbs or clauses."
            ),
            "examples": [
                {"zh": "电脑和书",               "pinyin": "diànnǎo hé shū",          "meaning": "computer and book"},
                {"zh": "爸爸和妈妈",             "pinyin": "bàba hé māma",             "meaning": "father and mother"},
                {"zh": "我有一个中国朋友和一个美国朋友。", "pinyin": "Wǒ yǒu yī gè Zhōngguó péngyou hé yī gè Měiguó péngyou.", "meaning": "I have a Chinese friend and an American friend."},
            ]
        },
        {
            "no": 3,
            "title_zh": "能愿动词 能 — Modal fe'l 能",
            "explanation": (
                "能(néng) — expresses ability or permission.\n"
                "Structure: Subject + 能 + Verb\n\n"
                "Example:\n"
                "我能坐这儿吗？— May I sit here?\n"
                "你能在这儿写名字吗？— Can you write your name here?\n\n"
                "能 vs 会:\n"
                "会 — ability acquired through learning (skill)\n"
                "能 — ability/permission based on circumstances (can/may)"
            ),
            "examples": [
                {"zh": "我能坐这儿吗？",       "pinyin": "Wǒ néng zuò zhèr ma?",       "meaning": "May I sit here?"},
                {"zh": "你能在这儿工作吗？",   "pinyin": "Nǐ néng zài zhèr gōngzuò ma?","meaning": "Can you work here?"},
                {"zh": "明天你能去商店吗？",   "pinyin": "Míngtiān nǐ néng qù shāngdiàn ma?","meaning": "Can you go to the store tomorrow?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "What is on the table?",                        "answer": "桌子上有什么？",             "pinyin": "Zhuōzi shàng yǒu shénme?"},
                {"prompt": "There is a book and a computer on the table.", "answer": "桌子上有一本书和一个电脑。", "pinyin": "Zhuōzi shàng yǒu yī běn shū hé yī gè diànnǎo."},
                {"prompt": "Is anyone sitting here?",                      "answer": "这儿有人吗？",               "pinyin": "Zhèr yǒu rén ma?"},
                {"prompt": "May I sit here?",                              "answer": "我能坐这儿吗？",             "pinyin": "Wǒ néng zuò zhèr ma?"},
                {"prompt": "Please, go ahead.",                            "answer": "请坐。",                     "pinyin": "Qǐng zuò."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "桌子上___一个电脑和一本书。", "answer": "有",   "pinyin": "yǒu"},
                {"prompt": "这儿有人吗？___。",          "answer": "没有", "pinyin": "méiyǒu"},
                {"prompt": "我___坐这儿吗？",             "answer": "能",   "pinyin": "néng"},
                {"prompt": "桌子上有电脑___书。",         "answer": "和",   "pinyin": "hé"},
            ]
        },
        {
            "no": 3,
            "type": "location",
            "instruction": "Say where it is (上/里/下面/前面/后面):",
            "items": [
                {"prompt": "Book — on the table",          "answer": "书在桌子上。",     "pinyin": "Shū zài zhuōzi shàng."},
                {"prompt": "Dog — under the chair",        "answer": "狗在椅子下面。",  "pinyin": "Gǒu zài yǐzi xiàmian."},
                {"prompt": "Computer — inside the desk",   "answer": "电脑在桌子里。",  "pinyin": "Diànnǎo zài zhuōzi lǐ."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["桌子上有什么？", "桌子上有一本书和一个电脑。", "这儿有人吗？", "我能坐这儿吗？", "请坐。"]},
        {"no": 2, "answers": ["有", "没有", "能", "和"]},
        {"no": 3, "answers": ["书在桌子上。", "狗在椅子下面。", "电脑在桌子里。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 4 sentences about your room (using 有):",
            "template": "我的桌子上有___。桌子里有___。椅子___有___。",
            "words": ["有", "没有", "上", "里", "下面", "电脑", "书", "杯子"],
        },
        {
            "no": 2,
            "instruction": "Write 3 questions using 能 and answer them:",
            "example": "A: 我能坐这儿吗？ B: 请坐。/ 对不起，不能。",
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
