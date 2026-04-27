import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 9,
    "lesson_code": "HSK1-L09",
    "title": "你儿子在哪儿工作",
    "goal": "Asking about location and workplace, the verb and preposition 在",
    "intro_text": (
        "In the ninth lesson you will learn to ask where someone is, "
        "where we work, and the two uses of 在. "
        "14 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "小",   "pinyin": "xiǎo",     "pos": "adj.", "meaning": "small, little"},
        {"no": 2,  "zh": "猫",   "pinyin": "māo",      "pos": "n.",   "meaning": "cat"},
        {"no": 3,  "zh": "在",   "pinyin": "zài",      "pos": "v./prep.", "meaning": "to be at / at, in (location marker)"},
        {"no": 4,  "zh": "哪儿", "pinyin": "nǎr",      "pos": "pron.", "meaning": "where"},
        {"no": 5,  "zh": "狗",   "pinyin": "gǒu",      "pos": "n.",   "meaning": "dog"},
        {"no": 6,  "zh": "椅子", "pinyin": "yǐzi",     "pos": "n.",   "meaning": "chair"},
        {"no": 7,  "zh": "下面", "pinyin": "xiàmian",  "pos": "n.",   "meaning": "below, underneath"},
        {"no": 8,  "zh": "工作", "pinyin": "gōngzuò",  "pos": "v./n.","meaning": "to work / work, job"},
        {"no": 9,  "zh": "儿子", "pinyin": "érzi",     "pos": "n.",   "meaning": "son"},
        {"no": 10, "zh": "医院", "pinyin": "yīyuàn",   "pos": "n.",   "meaning": "hospital"},
        {"no": 11, "zh": "医生", "pinyin": "yīshēng",  "pos": "n.",   "meaning": "doctor"},
        {"no": 12, "zh": "爸爸", "pinyin": "bàba",     "pos": "n.",   "meaning": "father, dad"},
        {"no": 13, "zh": "家",   "pinyin": "jiā",      "pos": "n.",   "meaning": "home, family"},
        {"no": 14, "zh": "那儿", "pinyin": "nàr",      "pos": "pron.", "meaning": "there, over there"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Uyda — mushuk va it qayerda",
            "dialogue": [
                {"speaker": "A", "zh": "小猫在哪儿？",          "pinyin": "Xiǎo māo zài nǎr?",           "translation": "Where is the cat?"},
                {"speaker": "B", "zh": "小猫在那儿。",          "pinyin": "Xiǎo māo zài nàr.",           "translation": "The cat is over there."},
                {"speaker": "A", "zh": "小狗在哪儿？",          "pinyin": "Xiǎo gǒu zài nǎr?",           "translation": "Where is the dog?"},
                {"speaker": "B", "zh": "小狗在椅子下面。",      "pinyin": "Xiǎo gǒu zài yǐzi xiàmian.",  "translation": "The dog is under the chair."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Temir yo'l stansiyasida — ish joyi",
            "dialogue": [
                {"speaker": "A", "zh": "你在哪儿工作？",              "pinyin": "Nǐ zài nǎr gōngzuò?",                      "translation": "Where do you work?"},
                {"speaker": "B", "zh": "我在学校工作。",              "pinyin": "Wǒ zài xuéxiào gōngzuò.",                  "translation": "I work at school."},
                {"speaker": "A", "zh": "你儿子在哪儿工作？",          "pinyin": "Nǐ érzi zài nǎr gōngzuò?",                 "translation": "Where does your son work?"},
                {"speaker": "B", "zh": "我儿子在医院工作，他是医生。", "pinyin": "Wǒ érzi zài yīyuàn gōngzuò, tā shì yīshēng.", "translation": "My son works at a hospital — he is a doctor."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Telefonda — ota qayerda",
            "dialogue": [
                {"speaker": "A", "zh": "你爸爸在家吗？",    "pinyin": "Nǐ bàba zài jiā ma?",  "translation": "Is your father home?"},
                {"speaker": "B", "zh": "不在家。",          "pinyin": "Bú zài jiā.",           "translation": "He is not home."},
                {"speaker": "A", "zh": "他在哪儿呢？",      "pinyin": "Tā zài nǎr ne?",        "translation": "Where is he then?"},
                {"speaker": "B", "zh": "他在医院。",        "pinyin": "Tā zài yīyuàn.",        "translation": "He is at the hospital."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "动词 在 — Fe'l 在 (joylashuv)",
            "explanation": (
                "在(zài) — as a verb, indicates where something/someone is located.\n"
                "Structure: Subject + 在 + Place\n\n"
                "Example:\n"
                "小猫在那儿。— The cat is over there.\n"
                "我朋友在学校。— My friend is at school.\n"
                "我妈妈在家。— My mother is at home.\n\n"
                "Negative: Subject + 不在 + Place\n"
                "爸爸不在家。— Father is not home."
            ),
            "examples": [
                {"zh": "小猫在那儿。",   "pinyin": "Xiǎo māo zài nàr.",     "meaning": "The cat is over there."},
                {"zh": "我朋友在学校。", "pinyin": "Wǒ péngyou zài xuéxiào.","meaning": "My friend is at school."},
                {"zh": "爸爸不在家。",   "pinyin": "Bàba bú zài jiā.",      "meaning": "Father is not home."},
            ]
        },
        {
            "no": 2,
            "title_zh": "哪儿 — Qayerda so'roq olmoshi",
            "explanation": (
                "哪儿(nǎr) — question word for asking about location.\n"
                "Structure: Subject + 在 + 哪儿?\n\n"
                "Example:\n"
                "小猫在哪儿？— Where is the cat?\n"
                "你在哪儿工作？— Where do you work?\n"
                "他在哪儿呢？— Where is he?"
            ),
            "examples": [
                {"zh": "你在哪儿工作？",  "pinyin": "Nǐ zài nǎr gōngzuò?",  "meaning": "Where do you work?"},
                {"zh": "小狗在哪儿？",    "pinyin": "Xiǎo gǒu zài nǎr?",    "meaning": "Where is the dog?"},
                {"zh": "他爸爸在哪儿呢？","pinyin": "Tā bàba zài nǎr ne?",   "meaning": "Where is his father?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "介词 在 — Predlog 在 (joy bildiradi)",
            "explanation": (
                "在(zài) — as a preposition, comes before a verb to indicate where an action takes place.\n"
                "Structure: Subject + 在 + Place + Verb\n\n"
                "Example:\n"
                "我儿子在医院工作。— My son works at the hospital.\n"
                "他们在学校看书。— They read at school.\n"
                "我在朋友家喝茶。— I am drinking tea at my friend's place.\n\n"
                "Difference:\n"
                "她在医院。(Verb 在) — She is at the hospital.\n"
                "她在医院工作。(Preposition 在) — She works at the hospital."
            ),
            "examples": [
                {"zh": "我儿子在医院工作。", "pinyin": "Wǒ érzi zài yīyuàn gōngzuò.",  "meaning": "My son works at the hospital."},
                {"zh": "他们在学校看书。",   "pinyin": "Tāmen zài xuéxiào kàn shū.",   "meaning": "They read at school."},
                {"zh": "我在家喝茶。",       "pinyin": "Wǒ zài jiā hē chá.",           "meaning": "I am drinking tea at home."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Where is the cat?",                        "answer": "小猫在哪儿？",               "pinyin": "Xiǎo māo zài nǎr?"},
                {"prompt": "The dog is under the chair.",              "answer": "小狗在椅子下面。",           "pinyin": "Xiǎo gǒu zài yǐzi xiàmian."},
                {"prompt": "Where do you work?",                       "answer": "你在哪儿工作？",             "pinyin": "Nǐ zài nǎr gōngzuò?"},
                {"prompt": "My son works at the hospital.",            "answer": "我儿子在医院工作。",         "pinyin": "Wǒ érzi zài yīyuàn gōngzuò."},
                {"prompt": "Is your father home?",                     "answer": "你爸爸在家吗？",             "pinyin": "Nǐ bàba zài jiā ma?"},
                {"prompt": "He is not home — he is at the hospital.",  "answer": "不在家，他在医院。",         "pinyin": "Bú zài jiā, tā zài yīyuàn."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "小猫___那儿。",              "answer": "在",   "pinyin": "zài"},
                {"prompt": "你___哪儿工作？",            "answer": "在",   "pinyin": "zài"},
                {"prompt": "小狗在椅子___面。",          "answer": "下",   "pinyin": "xià"},
                {"prompt": "我儿子在医院___，他是医生。", "answer": "工作", "pinyin": "gōngzuò"},
            ]
        },
        {
            "no": 3,
            "type": "make_sentence",
            "instruction": "Make a sentence from the given words:",
            "items": [
                {"words": ["在", "医院", "工作", "我妈妈"],        "answer": "我妈妈在医院工作。",  "pinyin": "Wǒ māma zài yīyuàn gōngzuò."},
                {"words": ["哪儿", "在", "小猫", "？"],            "answer": "小猫在哪儿？",        "pinyin": "Xiǎo māo zài nǎr?"},
                {"words": ["在", "家", "不", "爸爸"],              "answer": "爸爸不在家。",        "pinyin": "Bàba bú zài jiā."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["小猫在哪儿？", "小狗在椅子下面。", "你在哪儿工作？", "我儿子在医院工作。", "你爸爸在家吗？", "不在家，他在医院。"]},
        {"no": 2, "answers": ["在", "在", "下", "工作"]},
        {"no": 3, "answers": ["我妈妈在医院工作。", "小猫在哪儿？", "爸爸不在家。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 4 sentences about your family members (where they work/are):",
            "template": "我___在___工作/在___。",
            "words": ["在", "工作", "医院", "学校", "家", "商店"],
        },
        {
            "no": 2,
            "instruction": "Answer the questions:",
            "items": [
                {"prompt": "你在哪儿工作/学习？",  "hint": "Where do you work or study?"},
                {"prompt": "你爸爸在哪儿工作？",   "hint": "Where does your father work?"},
                {"prompt": "你现在在哪儿？",        "hint": "Where are you right now?"},
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
