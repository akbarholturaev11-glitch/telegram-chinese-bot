import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 12,
    "lesson_code": "HSK1-L12",
    "title": "明天天气怎么样",
    "goal": "Talking about the weather, the question word 怎么样, and the 太...了 construction",
    "intro_text": (
        "In lesson twelve you will learn how to talk about the weather, "
        "ask about states with 怎么样, and use the 太...了 construction. "
        "13 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "天气",  "pinyin": "tiānqì",   "pos": "n.",   "meaning": "weather"},
        {"no": 2,  "zh": "怎么样","pinyin": "zěnmeyàng","pos": "pron.","meaning": "how, what is it like"},
        {"no": 3,  "zh": "太",    "pinyin": "tài",      "pos": "adv.", "meaning": "too, extremely"},
        {"no": 4,  "zh": "热",    "pinyin": "rè",       "pos": "adj.", "meaning": "hot"},
        {"no": 5,  "zh": "冷",    "pinyin": "lěng",     "pos": "adj.", "meaning": "cold"},
        {"no": 6,  "zh": "下雨",  "pinyin": "xià yǔ",   "pos": "v.",   "meaning": "to rain"},
        {"no": 7,  "zh": "小姐",  "pinyin": "xiǎojiě",  "pos": "n.",   "meaning": "Miss, young lady"},
        {"no": 8,  "zh": "来",    "pinyin": "lái",      "pos": "v.",   "meaning": "to come"},
        {"no": 9,  "zh": "身体",  "pinyin": "shēntǐ",   "pos": "n.",   "meaning": "body, health"},
        {"no": 10, "zh": "爱",    "pinyin": "ài",       "pos": "v.",   "meaning": "to love, to like"},
        {"no": 11, "zh": "些",    "pinyin": "xiē",      "pos": "m.",   "meaning": "some, a few"},
        {"no": 12, "zh": "水果",  "pinyin": "shuǐguǒ",  "pos": "n.",   "meaning": "fruit"},
        {"no": 13, "zh": "水",    "pinyin": "shuǐ",     "pos": "n.",   "meaning": "water"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yo'lda — ob-havo muhokamasi",
            "dialogue": [
                {"speaker": "A", "zh": "昨天北京的天气怎么样？",    "pinyin": "Zuótiān Běijīng de tiānqì zěnmeyàng?",   "translation": "What was the weather like in Beijing yesterday?"},
                {"speaker": "B", "zh": "太热了。",                  "pinyin": "Tài rè le.",                             "translation": "It was extremely hot."},
                {"speaker": "A", "zh": "明天呢？明天天气怎么样？",  "pinyin": "Míngtiān ne? Míngtiān tiānqì zěnmeyàng?","translation": "What about tomorrow? What will the weather be like?"},
                {"speaker": "B", "zh": "明天天气很好，不冷不热。",  "pinyin": "Míngtiān tiānqì hěn hǎo, bù lěng bú rè.","translation": "Tomorrow the weather will be nice, neither cold nor hot."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sport zalda — yomg'ir va sovuq",
            "dialogue": [
                {"speaker": "A", "zh": "今天会下雨吗？",        "pinyin": "Jīntiān huì xià yǔ ma?",            "translation": "Will it rain today?"},
                {"speaker": "B", "zh": "今天不会下雨。",        "pinyin": "Jīntiān bú huì xià yǔ.",           "translation": "It won't rain today."},
                {"speaker": "A", "zh": "王小姐今天会来吗？",    "pinyin": "Wáng xiǎojiě jīntiān huì lái ma?", "translation": "Will Miss Wang come today?"},
                {"speaker": "B", "zh": "不会来，天气太冷了。",  "pinyin": "Bú huì lái, tiānqì tài lěng le.",  "translation": "She won't come, the weather is too cold."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kasalxonada — sog'liq haqida",
            "dialogue": [
                {"speaker": "A", "zh": "你身体怎么样？",                      "pinyin": "Nǐ shēntǐ zěnmeyàng?",                          "translation": "How is your health?"},
                {"speaker": "B", "zh": "我身体不太好。天气太热了，不爱吃饭。", "pinyin": "Wǒ shēntǐ bú tài hǎo. Tiānqì tài rè le, bú ài chī fàn.", "translation": "My health is not very good. The weather is too hot and I don't feel like eating."},
                {"speaker": "A", "zh": "你多吃些水果，多喝水。",              "pinyin": "Nǐ duō chī xiē shuǐguǒ, duō hē shuǐ.",          "translation": "Eat more fruit and drink more water."},
                {"speaker": "B", "zh": "谢谢你，医生。",                     "pinyin": "Xièxie nǐ, yīshēng.",                           "translation": "Thank you, doctor."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "怎么样 — Holat so'roq olmoshi",
            "explanation": (
                "怎么样(zěnmeyàng) — used to ask about a state, quality, or opinion.\n"
                "Structure: Subject + 怎么样?\n\n"
                "天气怎么样？— What is the weather like?\n"
                "你身体怎么样？— How is your health?\n"
                "你的汉语怎么样？— How is your Chinese?"
            ),
            "examples": [
                {"zh": "明天天气怎么样？", "pinyin": "Míngtiān tiānqì zěnmeyàng?", "meaning": "What will the weather be like tomorrow?"},
                {"zh": "你身体怎么样？",   "pinyin": "Nǐ shēntǐ zěnmeyàng?",      "meaning": "How is your health?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "太……了 — Haddan tashqari",
            "explanation": (
                "太(tài) + Adjective + 了 — 'too, extremely'\n"
                "Negative: 不太 + Adjective (no 了)\n\n"
                "天气太热了。— The weather is extremely hot.\n"
                "太冷了！— Too cold!\n"
                "我身体不太好。— My health is not very good."
            ),
            "examples": [
                {"zh": "太热了！",      "pinyin": "Tài rè le!",       "meaning": "Too hot!"},
                {"zh": "天气太冷了。",  "pinyin": "Tiānqì tài lěng le.", "meaning": "The weather is too cold."},
                {"zh": "我不太好。",    "pinyin": "Wǒ bú tài hǎo.",   "meaning": "I'm not doing very well."},
            ]
        },
        {
            "no": 3,
            "title_zh": "能愿动词 会 (2) — 会 ehtimollik bildiradi",
            "explanation": (
                "会 — indicates a likelihood of something happening in the future.\n\n"
                "今天会下雨吗？— Will it rain today?\n"
                "她会来吗？— Will she come?\n"
                "不会 — will not, won't happen"
            ),
            "examples": [
                {"zh": "今天会下雨吗？", "pinyin": "Jīntiān huì xià yǔ ma?", "meaning": "Will it rain today?"},
                {"zh": "明天会冷吗？",   "pinyin": "Míngtiān huì lěng ma?",  "meaning": "Will it be cold tomorrow?"},
                {"zh": "她今天不会来。", "pinyin": "Tā jīntiān bú huì lái.", "meaning": "She won't come today."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "What will the weather be like tomorrow?",   "answer": "明天天气怎么样？", "pinyin": "Míngtiān tiānqì zěnmeyàng?"},
                {"prompt": "The weather is extremely hot.",       "answer": "天气太热了。",     "pinyin": "Tiānqì tài rè le."},
                {"prompt": "Will it rain today?", "answer": "今天会下雨吗？",   "pinyin": "Jīntiān huì xià yǔ ma?"},
                {"prompt": "How is your health?",    "answer": "你身体怎么样？",   "pinyin": "Nǐ shēntǐ zěnmeyàng?"},
                {"prompt": "Eat more fruit.",        "answer": "多吃些水果。",     "pinyin": "Duō chī xiē shuǐguǒ."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "天气___热了。",    "answer": "太",     "pinyin": "tài"},
                {"prompt": "明天天气___？",    "answer": "怎么样", "pinyin": "zěnmeyàng"},
                {"prompt": "今天会___雨吗？",  "answer": "下",     "pinyin": "xià"},
                {"prompt": "我身体不___好。",  "answer": "太",     "pinyin": "tài"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["明天天气怎么样？", "天气太热了。", "今天会下雨吗？", "你身体怎么样？", "多吃些水果。"]},
        {"no": 2, "answers": ["太", "怎么样", "下", "太"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 3–4 sentences about today's weather:",
            "template": "今天天气___。天气___了。今天会___吗？",
            "words": ["天气", "太", "了", "热", "冷", "下雨", "怎么样"],
        },
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
