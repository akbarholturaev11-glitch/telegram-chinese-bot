import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 1,
    "lesson_code": "HSK3-L01",
    "title": "周末你有什么打算",
    "goal": "talking about weekend plans",
    "intro_text": "This lesson is dedicated to talking about weekend plans. It uses 5 key vocabulary words and covers core grammar patterns such as the resultative complement 好 and 一......也/都 + 不/没...... expressing negation.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "周末",
                        "pinyin": "zhōumò",
                        "pos": "n.",
                        "meaning": "weekend"
                },
                {
                        "no": 2,
                        "zh": "打算",
                        "pinyin": "dǎsuàn",
                        "pos": "v./n.",
                        "meaning": "to plan, plan"
                },
                {
                        "no": 3,
                        "zh": "作业",
                        "pinyin": "zuòyè",
                        "pos": "n.",
                        "meaning": "homework"
                },
                {
                        "no": 4,
                        "zh": "着急",
                        "pinyin": "zháojí",
                        "pos": "adj.",
                        "meaning": "worried, anxious"
                },
                {
                        "no": 5,
                        "zh": "地图",
                        "pinyin": "dìtú",
                        "pos": "n.",
                        "meaning": "map"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Weekend plan",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "周末你有什么打算？",
                                        "pinyin": "",
                                        "translation": "What are your plans for the weekend?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想先写作业，然后跟朋友出去。",
                                        "pinyin": "",
                                        "translation": "I want to do my homework first, then go out with a friend."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Preparing things",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "去公园要不要带地图？",
                                        "pinyin": "",
                                        "translation": "Do we need to bring a map to the park?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不用着急，我都准备好了。",
                                        "pinyin": "",
                                        "translation": "Don't worry, I've got everything ready."
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
                        "title_zh": "结果补语“好”",
                        "explanation": "This pattern indicates that an action has been completed successfully or satisfactorily.",
                        "examples": [
                                {
                                        "zh": "我准备好了。",
                                        "pinyin": "",
                                        "meaning": "I'm ready."
                                },
                                {
                                        "zh": "电影票买好了。",
                                        "pinyin": "",
                                        "meaning": "The movie tickets have been bought."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "一......也/都 + 不/没......表示否定",
                        "explanation": "This grammar topic helps to practice the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "周末你有什么打算。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有周末和打算。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 周末 and 打算."
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
                                        "prompt": "weekend",
                                        "answer": "周末",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt": "to plan, plan",
                                        "answer": "打算",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt": "homework",
                                        "answer": "作业",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt": "worried, anxious",
                                        "answer": "着急",
                                        "pinyin": "zháojí"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "周末",
                                        "answer": "weekend",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt": "打算",
                                        "answer": "to plan, plan",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt": "作业",
                                        "answer": "homework",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt": "着急",
                                        "answer": "worried, anxious",
                                        "pinyin": "zháojí"
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
                                "周末",
                                "打算",
                                "作业",
                                "着急"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "weekend",
                                "to plan, plan",
                                "homework",
                                "worried, anxious"
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
                                "周末",
                                "打算",
                                "作业"
                        ],
                        "example": "周末 和 打算 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "周末你有什么打算"
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
