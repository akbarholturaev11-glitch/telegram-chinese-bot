import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 6,
    "lesson_code": "HSK1-L06",
    "title": "我会说汉语",
    "goal": "Talking about abilities and skills, modal verb 会",
    "intro_text": (
        "In the sixth lesson you will learn to express abilities using the modal verb 会, "
        "adjective predicate sentences, and the question word 怎么. "
        "12 new words, 3 dialogues."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "会",   "pinyin": "huì",    "pos": "mod.", "meaning": "can, to be able to (through learning)"},
        {"no": 2,  "zh": "说",   "pinyin": "shuō",   "pos": "v.",   "meaning": "to speak, to say"},
        {"no": 3,  "zh": "妈妈", "pinyin": "māma",   "pos": "n.",   "meaning": "mother, mom"},
        {"no": 4,  "zh": "菜",   "pinyin": "cài",    "pos": "n.",   "meaning": "dish, food, vegetable"},
        {"no": 5,  "zh": "很",   "pinyin": "hěn",    "pos": "adv.", "meaning": "very, quite"},
        {"no": 6,  "zh": "好吃", "pinyin": "hǎochī", "pos": "adj.", "meaning": "delicious, tasty"},
        {"no": 7,  "zh": "做",   "pinyin": "zuò",    "pos": "v.",   "meaning": "to do, to make, to prepare"},
        {"no": 8,  "zh": "写",   "pinyin": "xiě",    "pos": "v.",   "meaning": "to write"},
        {"no": 9,  "zh": "汉字", "pinyin": "Hànzì",  "pos": "n.",   "meaning": "Chinese characters"},
        {"no": 10, "zh": "字",   "pinyin": "zì",     "pos": "n.",   "meaning": "character, letter"},
        {"no": 11, "zh": "怎么", "pinyin": "zěnme",  "pos": "pron.","meaning": "how, in what way"},
        {"no": 12, "zh": "读",   "pinyin": "dú",     "pos": "v.",   "meaning": "to read (aloud)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — xitoy tilida gapirish",
            "dialogue": [
                {"speaker": "A", "zh": "你会说汉语吗？",    "pinyin": "Nǐ huì shuō Hànyǔ ma?",     "translation": "Can you speak Chinese?"},
                {"speaker": "B", "zh": "我会说汉语。",      "pinyin": "Wǒ huì shuō Hànyǔ.",        "translation": "I can speak Chinese."},
                {"speaker": "A", "zh": "你妈妈会说汉语吗？", "pinyin": "Nǐ māma huì shuō Hànyǔ ma?", "translation": "Can your mother speak Chinese?"},
                {"speaker": "B", "zh": "她不会说。",        "pinyin": "Tā bú huì shuō.",            "translation": "She cannot speak it."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Oshxonada — xitoy taomi",
            "dialogue": [
                {"speaker": "A", "zh": "中国菜好吃吗？",    "pinyin": "Zhōngguó cài hǎochī ma?",    "translation": "Is Chinese food delicious?"},
                {"speaker": "B", "zh": "中国菜很好吃。",    "pinyin": "Zhōngguó cài hěn hǎochī.",   "translation": "Chinese food is very delicious."},
                {"speaker": "A", "zh": "你会做中国菜吗？",  "pinyin": "Nǐ huì zuò Zhōngguó cài ma?", "translation": "Can you cook Chinese food?"},
                {"speaker": "B", "zh": "我不会做。",        "pinyin": "Wǒ bú huì zuò.",             "translation": "I cannot cook it."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kutubxonada — xitoy yozuvi",
            "dialogue": [
                {"speaker": "A", "zh": "你会写汉字吗？",              "pinyin": "Nǐ huì xiě Hànzì ma?",                    "translation": "Can you write Chinese characters?"},
                {"speaker": "B", "zh": "我会写。",                    "pinyin": "Wǒ huì xiě.",                             "translation": "I can write them."},
                {"speaker": "A", "zh": "这个字怎么写？",              "pinyin": "Zhège zì zěnme xiě?",                     "translation": "How do you write this character?"},
                {"speaker": "B", "zh": "对不起，这个字我会读，不会写。", "pinyin": "Duìbuqǐ, zhège zì wǒ huì dú, bú huì xiě.", "translation": "Sorry, I can read this character but I cannot write it."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "能愿动词 会 — Modal fe'l 会",
            "explanation": (
                "会(huì) — expresses ability acquired through learning.\n"
                "Structure: Subject + (不)会 + Verb\n\n"
                "Affirmative: 我会说汉语。— I can speak Chinese.\n"
                "Negative: 我不会做中国菜。— I cannot cook Chinese food.\n"
                "Question: 你会写汉字吗？— Can you write Chinese characters?\n\n"
                "Note: Use 不会 for negation; use 吗 for yes/no questions."
            ),
            "examples": [
                {"zh": "我会说汉语。",     "pinyin": "Wǒ huì shuō Hànyǔ.",          "meaning": "I can speak Chinese."},
                {"zh": "她不会做中国菜。", "pinyin": "Tā bú huì zuò Zhōngguó cài.", "meaning": "She cannot cook Chinese food."},
                {"zh": "你会写汉字吗？",   "pinyin": "Nǐ huì xiě Hànzì ma?",        "meaning": "Can you write Chinese characters?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "形容词谓语句 — Sifat kesimli gap",
            "explanation": (
                "Adjective predicate: Subject + 很/不 + Adjective\n\n"
                "In Chinese, adjectives can serve as the predicate of a sentence.\n"
                "In affirmative sentences 很(hěn) is usually used:\n"
                "中国菜很好吃。— Chinese food is very delicious.\n\n"
                "In negative sentences 不 is used (很 is not required):\n"
                "我妈妈的汉语不好。— My mother's Chinese is not good.\n\n"
                "Note: 很 is often semantically weak and used to meet a grammatical requirement."
            ),
            "examples": [
                {"zh": "中国菜很好吃。",     "pinyin": "Zhōngguó cài hěn hǎochī.", "meaning": "Chinese food is very delicious."},
                {"zh": "她的汉语很好。",     "pinyin": "Tā de Hànyǔ hěn hǎo.",    "meaning": "Her Chinese is very good."},
                {"zh": "我妈妈的汉语不好。", "pinyin": "Wǒ māma de Hànyǔ bù hǎo.", "meaning": "My mother's Chinese is not good."},
            ]
        },
        {
            "no": 3,
            "title_zh": "怎么 — Qanday so'roq olmoshi",
            "explanation": (
                "怎么(zěnme) — placed before a verb, asks about the manner of an action.\n"
                "Structure: Subject + 怎么 + Verb?\n\n"
                "Example:\n"
                "这个字怎么写？— How do you write this character?\n"
                "这个字怎么读？— How do you read this character?\n"
                "中国菜怎么做？— How do you cook Chinese food?"
            ),
            "examples": [
                {"zh": "这个字怎么写？", "pinyin": "Zhège zì zěnme xiě?", "meaning": "How do you write this character?"},
                {"zh": "这个字怎么读？", "pinyin": "Zhège zì zěnme dú?",  "meaning": "How do you read this character?"},
                {"zh": "汉语怎么说？",   "pinyin": "Hànyǔ zěnme shuō?",  "meaning": "How do you say it in Chinese?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Write in Chinese:",
            "items": [
                {"prompt": "Can you speak Chinese?",              "answer": "你会说汉语吗？",   "pinyin": "Nǐ huì shuō Hànyǔ ma?"},
                {"prompt": "I can speak Chinese.",                "answer": "我会说汉语。",     "pinyin": "Wǒ huì shuō Hànyǔ."},
                {"prompt": "Chinese food is very delicious.",     "answer": "中国菜很好吃。",   "pinyin": "Zhōngguó cài hěn hǎochī."},
                {"prompt": "I cannot cook Chinese food.",         "answer": "我不会做中国菜。", "pinyin": "Wǒ bú huì zuò Zhōngguó cài."},
                {"prompt": "How do you write this character?",    "answer": "这个字怎么写？",   "pinyin": "Zhège zì zěnme xiě?"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Fill in the blank:",
            "items": [
                {"prompt": "你___说汉语吗？",     "answer": "会",   "pinyin": "huì"},
                {"prompt": "中国菜___好吃。",     "answer": "很",   "pinyin": "hěn"},
                {"prompt": "这个字___写？",       "answer": "怎么", "pinyin": "zěnme"},
                {"prompt": "我会___，不会___。",  "answer": "读/写", "pinyin": "dú/xiě"},
            ]
        },
        {
            "no": 3,
            "type": "make_negative",
            "instruction": "Turn into a negative sentence:",
            "items": [
                {"prompt": "我会说汉语。",   "answer": "我不会说汉语。",   "pinyin": "Wǒ bú huì shuō Hànyǔ."},
                {"prompt": "中国菜很好吃。", "answer": "中国菜不好吃。",   "pinyin": "Zhōngguó cài bù hǎochī."},
                {"prompt": "她会写汉字。",   "answer": "她不会写汉字。",   "pinyin": "Tā bú huì xiě Hànzì."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你会说汉语吗？", "我会说汉语。", "中国菜很好吃。", "我不会做中国菜。", "这个字怎么写？"]},
        {"no": 2, "answers": ["会", "很", "怎么", "读/写"]},
        {"no": 3, "answers": ["我不会说汉语。", "中国菜不好吃。", "她不会写汉字。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Write 4 sentences about yourself (what you can/cannot do):",
            "template": "我会___。我不会___。我___会___吗？",
            "words": ["会", "不会", "说", "写", "做", "读", "汉语", "汉字", "中国菜"],
        },
        {
            "no": 2,
            "instruction": "Answer the questions:",
            "items": [
                {"prompt": "你会说汉语吗？",      "hint": "Yes or no, with a full sentence"},
                {"prompt": "中国菜好吃吗？",      "hint": "Share your own opinion"},
                {"prompt": "这个字怎么写？ (好)", "hint": "Describe how to write the character Hǎo — good"},
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
