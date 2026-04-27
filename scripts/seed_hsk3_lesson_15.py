import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 15,
    "lesson_code": "HSK3-L15",
    "title": "其他都没什么问题",
    "goal": "expressing exceptions, remaining things, and degree",
    "intro_text": "This lesson focuses on expressing exceptions, remaining things, and degree. It uses 5 key vocabulary words and covers the main grammar patterns 除了……以外，都/还/也…… and 程度的表达：极了.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "留学",
                        "pinyin": "liúxué",
                        "pos": "v.",
                        "meaning": "to study abroad"
                },
                {
                        "no": 2,
                        "zh": "水平",
                        "pinyin": "shuǐpíng",
                        "pos": "n.",
                        "meaning": "level, standard"
                },
                {
                        "no": 3,
                        "zh": "提高",
                        "pinyin": "tígāo",
                        "pos": "v.",
                        "meaning": "to improve, to raise"
                },
                {
                        "no": 4,
                        "zh": "新闻",
                        "pinyin": "xīnwén",
                        "pos": "n.",
                        "meaning": "news"
                },
                {
                        "no": 5,
                        "zh": "文化",
                        "pinyin": "wénhuà",
                        "pos": "n.",
                        "meaning": "culture"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Checking a plan",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "translation": "Everything else is pretty much fine."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那我们就按计划进行吧。",
                                        "pinyin": "",
                                        "translation": "Then let's proceed according to plan."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Study abroad",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "除了语言以外，你还担心什么？",
                                        "pinyin": "",
                                        "translation": "Besides language, what else are you worried about?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我最想提高自己的文化水平。",
                                        "pinyin": "",
                                        "translation": "What I want most is to improve my cultural knowledge."
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
                        "title_zh": "除了……以外，都/还/也……",
                        "explanation": "This grammar topic helps practice the main sentence patterns used in the lesson.",
                        "examples": [
                                {
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有留学和水平。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 留学 and 水平."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "程度的表达：极了",
                        "explanation": "This grammar topic helps practice the main sentence patterns used in the lesson.",
                        "examples": [
                                {
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有留学和水平。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 留学 and 水平."
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
                                        "prompt": "to study abroad",
                                        "answer": "留学",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt": "level, standard",
                                        "answer": "水平",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt": "to improve, to raise",
                                        "answer": "提高",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt": "news",
                                        "answer": "新闻",
                                        "pinyin": "xīnwén"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "留学",
                                        "answer": "to study abroad",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt": "水平",
                                        "answer": "level, standard",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt": "提高",
                                        "answer": "to improve, to raise",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt": "新闻",
                                        "answer": "news",
                                        "pinyin": "xīnwén"
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
                                "留学",
                                "水平",
                                "提高",
                                "新闻"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "to study abroad",
                                "level, standard",
                                "to improve, to raise",
                                "news"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Make 3 sentences using the following words:",
                        "words": [
                                "留学",
                                "水平",
                                "提高"
                        ],
                        "example": "留学 和 水平 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short text of 4-5 sentences about the lesson topic:",
                        "topic": "其他都没什么问题"
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
