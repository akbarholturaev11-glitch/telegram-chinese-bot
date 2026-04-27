import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 2,
    "lesson_code": "HSK3-L02",
    "title": "他什么时候回来",
    "goal": "expressing returning and sequential actions",
    "intro_text": "This lesson is dedicated to expressing returning and sequential actions. It uses 5 key vocabulary words and covers core grammar patterns such as simple directional complements and two actions occurring in succession.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "回来",
                        "pinyin": "huílai",
                        "pos": "v.",
                        "meaning": "to come back"
                },
                {
                        "no": 2,
                        "zh": "办公室",
                        "pinyin": "bàngōngshì",
                        "pos": "n.",
                        "meaning": "office"
                },
                {
                        "no": 3,
                        "zh": "拿",
                        "pinyin": "ná",
                        "pos": "v.",
                        "meaning": "to take, to get"
                },
                {
                        "no": 4,
                        "zh": "伞",
                        "pinyin": "sǎn",
                        "pos": "n.",
                        "meaning": "umbrella"
                },
                {
                        "no": 5,
                        "zh": "腿",
                        "pinyin": "tuǐ",
                        "pos": "n.",
                        "meaning": "leg"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Waiting in the office",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "他什么时候回来？",
                                        "pinyin": "",
                                        "translation": "When will he come back?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他先去办公室拿文件，马上就回来。",
                                        "pinyin": "",
                                        "translation": "He went to the office to get some documents first, he'll be back shortly."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On a rainy day",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "外边下雨了，你把伞拿回来了吗？",
                                        "pinyin": "",
                                        "translation": "It's raining outside, did you bring the umbrella back?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "拿回来了，不过我的腿还有点儿疼。",
                                        "pinyin": "",
                                        "translation": "I brought it back, but my leg still hurts a little."
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
                        "title_zh": "简单趋向补语",
                        "explanation": "This topic shows the direction of movement of an action, or where the subject ends up as a result.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 回来 and 办公室."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "两个动作连续发生",
                        "explanation": "This grammar topic helps to practice the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 回来 and 办公室."
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
                                        "prompt": "to come back",
                                        "answer": "回来",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt": "office",
                                        "answer": "办公室",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt": "to take, to get",
                                        "answer": "拿",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt": "umbrella",
                                        "answer": "伞",
                                        "pinyin": "sǎn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "回来",
                                        "answer": "to come back",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt": "办公室",
                                        "answer": "office",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt": "拿",
                                        "answer": "to take, to get",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt": "伞",
                                        "answer": "umbrella",
                                        "pinyin": "sǎn"
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
                                "回来",
                                "办公室",
                                "拿",
                                "伞"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "to come back",
                                "office",
                                "to take, to get",
                                "umbrella"
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
                                "回来",
                                "办公室",
                                "拿"
                        ],
                        "example": "回来 和 办公室 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "他什么时候回来"
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
