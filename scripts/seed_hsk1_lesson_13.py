import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 13,
    "lesson_code": "HSK1-L13",
    "title": "他在学做中国菜呢",
    "goal": "Expressing ongoing actions (在...呢), phone numbers, and the particle 吧",
    "intro_text": (
        "In lesson thirteen you will learn how to express actions happening right now, "
        "use the 在...呢 construction, and the particle 吧. "
        "10 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "喂",   "pinyin": "wèi",      "pos": "int.", "meaning": "hello (on the phone)"},
        {"no": 2,  "zh": "也",   "pinyin": "yě",       "pos": "adv.", "meaning": "also, too"},
        {"no": 3,  "zh": "学习", "pinyin": "xuéxí",    "pos": "v.",   "meaning": "to study, to learn"},
        {"no": 4,  "zh": "上午", "pinyin": "shàngwǔ",  "pos": "n.",   "meaning": "morning (before noon)"},
        {"no": 5,  "zh": "睡觉", "pinyin": "shuì jiào","pos": "v.",   "meaning": "to sleep"},
        {"no": 6,  "zh": "电视", "pinyin": "diànshì",  "pos": "n.",   "meaning": "television"},
        {"no": 7,  "zh": "喜欢", "pinyin": "xǐhuan",   "pos": "v.",   "meaning": "to like, to enjoy"},
        {"no": 8,  "zh": "给",   "pinyin": "gěi",      "pos": "prep.","meaning": "to, for (someone)"},
        {"no": 9,  "zh": "打电话","pinyin": "dǎ diànhuà","pos": "v.",  "meaning": "to make a phone call"},
        {"no": 10, "zh": "吧",   "pinyin": "ba",       "pos": "part.","meaning": "softening particle for suggestions or mild commands"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Telefonda — hozir nima qilyapsan",
            "dialogue": [
                {"speaker": "A", "zh": "喂，你在做什么呢？",              "pinyin": "Wèi, nǐ zài zuò shénme ne?",                    "translation": "Hello, what are you doing right now?"},
                {"speaker": "B", "zh": "我在看书呢。",                    "pinyin": "Wǒ zài kàn shū ne.",                            "translation": "I'm reading a book right now."},
                {"speaker": "A", "zh": "大卫也在看书吗？",                "pinyin": "Dàwèi yě zài kàn shū ma?",                     "translation": "Is David reading too?"},
                {"speaker": "B", "zh": "他没看书，他在学做中国菜呢。",    "pinyin": "Tā méi kàn shū, tā zài xué zuò Zhōngguó cài ne.", "translation": "He is not reading; he is learning to cook Chinese food."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Qahvaxonada — kecha nima qilding",
            "dialogue": [
                {"speaker": "A", "zh": "昨天上午你在做什么呢？",          "pinyin": "Zuótiān shàngwǔ nǐ zài zuò shénme ne?",         "translation": "What were you doing yesterday morning?"},
                {"speaker": "B", "zh": "我在睡觉呢。你呢？",              "pinyin": "Wǒ zài shuì jiào ne. Nǐ ne?",                  "translation": "I was sleeping. What about you?"},
                {"speaker": "A", "zh": "我在家看电视呢。你喜欢看电视吗？","pinyin": "Wǒ zài jiā kàn diànshì ne. Nǐ xǐhuan kàn diànshì ma?", "translation": "I was watching TV at home. Do you like watching TV?"},
                {"speaker": "B", "zh": "我不喜欢看电视，我喜欢看电影。",  "pinyin": "Wǒ bù xǐhuan kàn diànshì, wǒ xǐhuan kàn diànyǐng.", "translation": "I don't like watching TV; I like watching movies."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Maktab ofisida — telefon raqami",
            "dialogue": [
                {"speaker": "A", "zh": "82304155，这是李老师的电话吗？",     "pinyin": "Bā èr sān líng sì yāo wǔ wǔ, zhè shì Lǐ lǎoshī de diànhuà ma?", "translation": "82304155, is this Teacher Li's phone number?"},
                {"speaker": "B", "zh": "不是。她的电话是82304156。",         "pinyin": "Bú shì. Tā de diànhuà shì bā èr sān líng sì yāo wǔ liù.",      "translation": "No. Her number is 82304156."},
                {"speaker": "A", "zh": "好，我现在给她打电话。",             "pinyin": "Hǎo, wǒ xiànzài gěi tā dǎ diànhuà.",                           "translation": "OK, I'll call her now."},
                {"speaker": "B", "zh": "她在工作呢，你下午打吧。",           "pinyin": "Tā zài gōngzuò ne, nǐ xiàwǔ dǎ ba.",                          "translation": "She is working right now; call in the afternoon."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "在……呢 — Hozirgi davom harakat",
            "explanation": (
                "For an action in progress right now:\n"
                "Structure 1: 在 + Verb (+ Object)\n"
                "Structure 2: Verb + Object + 呢\n"
                "Structure 3: 在 + Verb + 呢 (emphatic)\n\n"
                "Example:\n"
                "我在看书呢。— I am reading a book right now.\n"
                "他在学做中国菜呢。— He is learning to cook Chinese food.\n\n"
                "Negation: 没(在) + Verb, no 呢\n"
                "他没看书。— He is not reading.\n"
                "他们没在工作。— They are not working."
            ),
            "examples": [
                {"zh": "我在看书呢。",         "pinyin": "Wǒ zài kàn shū ne.",           "meaning": "I am reading a book right now."},
                {"zh": "他在学做中国菜呢。",   "pinyin": "Tā zài xué zuò Zhōngguó cài ne.", "meaning": "He is learning to cook Chinese food."},
                {"zh": "她没在工作。",         "pinyin": "Tā méi zài gōngzuò.",          "meaning": "She is not working."},
            ]
        },
        {
            "no": 2,
            "title_zh": "也 — Ham ravishi",
            "explanation": (
                "也(yě) — means 'also, too'.\n"
                "Always comes before the verb or modal verb.\n\n"
                "Example:\n"
                "大卫也在看书吗？— Is David reading too?\n"
                "我也喜欢看电影。— I also like watching movies.\n"
                "她也是老师。— She is also a teacher."
            ),
            "examples": [
                {"zh": "大卫也在看书吗？",   "pinyin": "Dàwèi yě zài kàn shū ma?",   "meaning": "Is David reading too?"},
                {"zh": "我也喜欢中国菜。",   "pinyin": "Wǒ yě xǐhuan Zhōngguó cài.", "meaning": "I also like Chinese food."},
                {"zh": "她也是学生。",       "pinyin": "Tā yě shì xuésheng.",         "meaning": "She is also a student."},
            ]
        },
        {
            "no": 3,
            "title_zh": "吧 — Yumshatuvchi yukla",
            "explanation": (
                "吧(ba) — expresses a suggestion, advice, or softened command.\n"
                "Comes at the end of the sentence.\n\n"
                "Example:\n"
                "你下午打吧。— Call in the afternoon.\n"
                "今天我们在家吃饭吧。— Let's eat at home today.\n"
                "请坐吧。— Please have a seat."
            ),
            "examples": [
                {"zh": "你下午打吧。",           "pinyin": "Nǐ xiàwǔ dǎ ba.",           "meaning": "Call in the afternoon."},
                {"zh": "我们一起去吧。",         "pinyin": "Wǒmen yīqǐ qù ba.",         "meaning": "Let's go together."},
                {"zh": "请坐吧。",               "pinyin": "Qǐng zuò ba.",               "meaning": "Please have a seat."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "What are you doing right now?",               "answer": "你在做什么呢？",          "pinyin": "Nǐ zài zuò shénme ne?"},
                {"prompt": "I am reading a book right now.",          "answer": "我在看书呢。",             "pinyin": "Wǒ zài kàn shū ne."},
                {"prompt": "He is not working.",                   "answer": "他没在工作。",             "pinyin": "Tā méi zài gōngzuò."},
                {"prompt": "I also like watching movies.",   "answer": "我也喜欢看电影。",         "pinyin": "Wǒ yě xǐhuan kàn diànyǐng."},
                {"prompt": "I'll call her now.",          "answer": "我现在给她打电话。",       "pinyin": "Wǒ xiànzài gěi tā dǎ diànhuà."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "我___看书呢。",               "answer": "在",   "pinyin": "zài"},
                {"prompt": "大卫___在看书吗？",           "answer": "也",   "pinyin": "yě"},
                {"prompt": "他没___书，他在学做菜呢。",   "answer": "看",   "pinyin": "kàn"},
                {"prompt": "你下午打___。",               "answer": "吧",   "pinyin": "ba"},
            ]
        },
        {
            "no": 3,
            "type": "phone_numbers",
            "instruction": "Read the phone numbers aloud in Chinese:",
            "items": [
                {"prompt": "8069478",    "answer": "bā líng liù jiǔ sì qī bā"},
                {"prompt": "13851897623","answer": "yāo sān bā wǔ yāo bā jiǔ liù èr sān"},
                {"prompt": "82304156",   "answer": "bā èr sān líng sì yāo wǔ liù"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你在做什么呢？", "我在看书呢。", "他没在工作。", "我也喜欢看电影。", "我现在给她打电话。"]},
        {"no": 2, "answers": ["在", "也", "看", "吧"]},
        {"no": 3, "answers": ["bā líng liù jiǔ sì qī bā", "yāo sān bā wǔ yāo bā jiǔ liù èr sān", "bā èr sān líng sì yāo wǔ liù"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "What were you doing yesterday morning? Write 3–4 sentences:",
            "template": "昨天上午我在___呢。我___喜欢___。",
            "words": ["在", "呢", "也", "喜欢", "看书", "看电视", "睡觉", "学习"],
        },
        {
            "no": 2,
            "instruction": "Write a phone call dialogue with a friend (4 lines, start with 喂):",
            "example": "A: 喂，你在做什么呢？\nB: 我在___呢。\nA: ___也在___吗？\nB: 她___，她在___呢。",
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
