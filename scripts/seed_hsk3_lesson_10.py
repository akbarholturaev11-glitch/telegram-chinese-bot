import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 10,
    "lesson_code": "HSK3-L10",
    "title": "数学比历史难多了",
    "goal": "expressing comparison and difference in degree",
    "intro_text": "This lesson is dedicated to expressing comparison and difference in degree. It introduces 5 key vocabulary words and covers core grammar patterns such as 比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了 and 概数的表达 1.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "数学",
                        "pinyin": "shùxué",
                        "pos": "n.",
                        "meaning": "mathematics"
                },
                {
                        "no": 2,
                        "zh": "历史",
                        "pinyin": "lìshǐ",
                        "pos": "n.",
                        "meaning": "history"
                },
                {
                        "no": 3,
                        "zh": "体育",
                        "pinyin": "tǐyù",
                        "pos": "n.",
                        "meaning": "physical education / sports"
                },
                {
                        "no": 4,
                        "zh": "自行车",
                        "pinyin": "zìxíngchē",
                        "pos": "n.",
                        "meaning": "bicycle"
                },
                {
                        "no": 5,
                        "zh": "附近",
                        "pinyin": "fùjìn",
                        "pos": "n.",
                        "meaning": "nearby; in the vicinity"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "About subjects",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "translation": "Math is much harder than history."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我觉得体育比数学轻松一些。",
                                        "pinyin": "",
                                        "translation": "I think PE is a bit more relaxed than math."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On the way",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "学校离你家远吗？",
                                        "pinyin": "",
                                        "translation": "Is the school far from your home?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不太远，骑自行车二十分钟左右。",
                                        "pinyin": "",
                                        "translation": "Not too far — about twenty minutes by bicycle."
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
                {
                        "no": 1,
                        "title_zh": "比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了",
                        "explanation": "This pattern is used to compare two things or people in terms of degree.",
                        "examples": [
                                {
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "meaning": "A comparison example from the lesson title."
                                },
                                {
                                        "zh": "数学比历史更重要。",
                                        "pinyin": "",
                                        "meaning": "数学 is even more important than 历史."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 1",
                        "explanation": "This topic helps express approximate numbers or time in a soft, flexible way.",
                        "examples": [
                                {
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "meaning": "The key pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有数学和历史。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 数学 and 历史."
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "exercise_json": json.dumps(
        [
                {
                        "no": 1,
                        "type": "translate_to_chinese",
                        "instruction": "Write the Chinese for the following meanings:",
                        "items": [
                                {
                                        "prompt": "mathematics",
                                        "answer": "数学",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt": "history",
                                        "answer": "历史",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt": "physical education / sports",
                                        "answer": "体育",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt": "bicycle",
                                        "answer": "自行车",
                                        "pinyin": "zìxíngchē"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "数学",
                                        "answer": "mathematics",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt": "历史",
                                        "answer": "history",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt": "体育",
                                        "answer": "physical education / sports",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt": "自行车",
                                        "answer": "bicycle",
                                        "pinyin": "zìxíngchē"
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
                {
                        "no": 1,
                        "answers": [
                                "数学",
                                "历史",
                                "体育",
                                "自行车"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "mathematics",
                                "history",
                                "physical education / sports",
                                "bicycle"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Write 3 sentences using the following words:",
                        "words": [
                                "数学",
                                "历史",
                                "体育"
                        ],
                        "example": "数学 和 历史 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short passage of 4–5 sentences about the lesson topic:",
                        "topic": "数学比历史难多了"
                }
        ],
        ensure_ascii=False,
    ),
    "review_json": "[]",
    "is_active": True
}


async def upsert_lesson():
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.level = LESSON["level"]
            existing.lesson_order = LESSON["lesson_order"]
            existing.title = LESSON["title"]
            existing.goal = LESSON["goal"]
            existing.intro_text = LESSON["intro_text"]
            existing.vocabulary_json = LESSON["vocabulary_json"]
            existing.dialogue_json = LESSON["dialogue_json"]
            existing.grammar_json = LESSON["grammar_json"]
            existing.exercise_json = LESSON["exercise_json"]
            existing.answers_json = LESSON["answers_json"]
            existing.homework_json = LESSON["homework_json"]
            existing.review_json = LESSON["review_json"]
            existing.is_active = LESSON["is_active"]
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
