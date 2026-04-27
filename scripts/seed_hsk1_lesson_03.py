import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 3,
    "lesson_code": "HSK1-L03",
    "title": "你叫什么名字",
    "goal": "Learn to say your name, nationality, and occupation in Chinese",
    "intro_text": (
        "In the third lesson you will learn how to say your name, "
        "your nationality, and your occupation in Chinese. "
        "9 new words, 3 dialogues, and grammar for 是-sentences."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "叫",   "pinyin": "jiào",     "pos": "v.",    "meaning": "to be called, to call"},
        {"no": 2, "zh": "什么", "pinyin": "shénme",   "pos": "pron.", "meaning": "what, which"},
        {"no": 3, "zh": "名字", "pinyin": "míngzi",   "pos": "n.",    "meaning": "name"},
        {"no": 4, "zh": "我",   "pinyin": "wǒ",       "pos": "pron.", "meaning": "I, me"},
        {"no": 5, "zh": "是",   "pinyin": "shì",      "pos": "v.",    "meaning": "to be (=)"},
        {"no": 6, "zh": "老师", "pinyin": "lǎoshī",   "pos": "n.",    "meaning": "teacher"},
        {"no": 7, "zh": "吗",   "pinyin": "ma",       "pos": "part.", "meaning": "question particle"},
        {"no": 8, "zh": "学生", "pinyin": "xuésheng", "pos": "n.",    "meaning": "student"},
        {"no": 9, "zh": "人",   "pinyin": "rén",      "pos": "n.",    "meaning": "person, people"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — ism so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你叫什么名字？",  "pinyin": "Nǐ jiào shénme míngzi?", "translation": "What is your name?"},
                {"speaker": "B", "zh": "我叫李月。",      "pinyin": "Wǒ jiào Lǐ Yuè.",        "translation": "My name is Li Yue."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sinfda — kasb so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是老师吗？",          "pinyin": "Nǐ shì lǎoshī ma?",             "translation": "Are you a teacher?"},
                {"speaker": "B", "zh": "我不是老师，我是学生。", "pinyin": "Wǒ bú shì lǎoshī, wǒ shì xuésheng.", "translation": "I am not a teacher, I am a student."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Maktabda — millat so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是中国人吗？",           "pinyin": "Nǐ shì Zhōngguó rén ma?",               "translation": "Are you Chinese?"},
                {"speaker": "B", "zh": "我不是中国人，我是美国人。", "pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén.", "translation": "I am not Chinese, I am American."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "是字句 — 是 gapi",
            "explanation": (
                "是(shì) — expresses equality (= to be).\n"
                "Structure: Subject + 是 + Noun/Noun phrase\n"
                "Negation: Subject + 不是 + Noun/Noun phrase\n\n"
                "Example:\n"
                "我是老师。— I am a teacher.\n"
                "我不是老师。— I am not a teacher.\n"
                "李月是中国人。— Li Yue is Chinese."
            ),
            "examples": [
                {"zh": "我是学生。",     "pinyin": "Wǒ shì xuésheng.",     "meaning": "I am a student."},
                {"zh": "我不是老师。",   "pinyin": "Wǒ bú shì lǎoshī.",    "meaning": "I am not a teacher."},
                {"zh": "她是中国人。",   "pinyin": "Tā shì Zhōngguó rén.", "meaning": "She is Chinese."},
            ]
        },
        {
            "no": 2,
            "title_zh": "吗 — So'roq gapi",
            "explanation": (
                "吗(ma) — placed at the end of a sentence turns it into a yes/no question.\n"
                "Structure: Statement + 吗？\n\n"
                "Example:\n"
                "你是老师。→ 你是老师吗？\n"
                "You are a teacher. → Are you a teacher?\n\n"
                "Answer: 是 (yes) or 不是 (no)"
            ),
            "examples": [
                {"zh": "你是学生吗？",   "pinyin": "Nǐ shì xuésheng ma?",   "meaning": "Are you a student?"},
                {"zh": "你是美国人吗？", "pinyin": "Nǐ shì Měiguó rén ma?", "meaning": "Are you American?"},
                {"zh": "你叫李月吗？",   "pinyin": "Nǐ jiào Lǐ Yuè ma?",   "meaning": "Is your name Li Yue?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "什么 — So'roq olmoshi",
            "explanation": (
                "什么(shénme) — means 'what', 'which'.\n"
                "Do not add 吗 at the end — 什么 itself makes the sentence a question.\n\n"
                "Example:\n"
                "你叫什么名字？— What is your name?\n"
                "这是什么？— What is this?\n"
                "你是什么人？— Who are you?"
            ),
            "examples": [
                {"zh": "你叫什么名字？", "pinyin": "Nǐ jiào shénme míngzi?", "meaning": "What is your name?"},
                {"zh": "这是什么？",     "pinyin": "Zhè shì shénme?",        "meaning": "What is this?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "What is your name?",                          "answer": "你叫什么名字？",          "pinyin": "Nǐ jiào shénme míngzi?"},
                {"prompt": "My name is Wang Fang.",                       "answer": "我叫王芳。",               "pinyin": "Wǒ jiào Wáng Fāng."},
                {"prompt": "Are you a teacher?",                          "answer": "你是老师吗？",             "pinyin": "Nǐ shì lǎoshī ma?"},
                {"prompt": "I am a student.",                              "answer": "我是学生。",               "pinyin": "Wǒ shì xuésheng."},
                {"prompt": "I am not Chinese, I am American.",            "answer": "我不是中国人，我是美国人。","pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "A: 你叫___名字？  B: 我叫李月。",         "answer": "什么",  "pinyin": "shénme"},
                {"prompt": "A: 你___老师吗？  B: 是，我是老师。",     "answer": "是",    "pinyin": "shì"},
                {"prompt": "A: 你是中国人___？ B: 不是，我是美国人。", "answer": "吗",    "pinyin": "ma"},
                {"prompt": "我不___老师，我是学生。",                   "answer": "是",    "pinyin": "shì"},
            ]
        },
        {
            "no": 3,
            "type": "make_question",
            "instruction": "Turn into a question using 吗:",
            "items": [
                {"prompt": "你是学生。",     "answer": "你是学生吗？",   "pinyin": "Nǐ shì xuésheng ma?"},
                {"prompt": "他是中国人。",   "answer": "他是中国人吗？", "pinyin": "Tā shì Zhōngguó rén ma?"},
                {"prompt": "她叫李月。",     "answer": "她叫李月吗？",   "pinyin": "Tā jiào Lǐ Yuè ma?"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你叫什么名字？", "我叫王芳。", "你是老师吗？", "我是学生。", "我不是中国人，我是美国人。"]},
        {"no": 2, "answers": ["什么", "是", "吗", "是"]},
        {"no": 3, "answers": ["你是学生吗？", "他是中国人吗？", "她叫李月吗？"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 3 sentences about yourself (name, nationality, occupation):",
            "example": "我叫___。我是___人。我是___。",
            "words": ["叫", "是", "不是", "老师", "学生", "中国人", "美国人"],
        },
        {
            "no": 2,
            "instruction": "Turn the following sentences into questions using 吗:",
            "items": [
                {"prompt": "你是老师。",   "answer": "你是老师吗？"},
                {"prompt": "他叫大卫。",   "answer": "他叫大卫吗？"},
                {"prompt": "她是美国人。", "answer": "她是美国人吗？"},
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
