import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 16,
    "lesson_code": "HSK3-L16",
    "title": "我现在累得下了班就想睡觉",
    "goal": "expressing resultative states and conditions",
    "intro_text": "This lesson focuses on expressing resultative states and conditions. It uses 5 key vocabulary words and covers the main grammar patterns 如果……（的话），（S）就…… and 复杂的状态补语.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "累",
                        "pinyin": "lèi",
                        "pos": "adj.",
                        "meaning": "tired"
                },
                {
                        "no": 2,
                        "zh": "睡觉",
                        "pinyin": "shuìjiào",
                        "pos": "v.",
                        "meaning": "to sleep"
                },
                {
                        "no": 3,
                        "zh": "如果",
                        "pinyin": "rúguǒ",
                        "pos": "conj.",
                        "meaning": "if"
                },
                {
                        "no": 4,
                        "zh": "城市",
                        "pinyin": "chéngshì",
                        "pos": "n.",
                        "meaning": "city"
                },
                {
                        "no": 5,
                        "zh": "检查",
                        "pinyin": "jiǎnchá",
                        "pos": "v.",
                        "meaning": "to check, to inspect"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "After work",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你今天怎么这么累？",
                                        "pinyin": "",
                                        "translation": "Why are you so tired today?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "",
                                        "translation": "I'm so tired right now that after work I just want to sleep."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Advice",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "如果你这么累，就早点休息吧。",
                                        "pinyin": "",
                                        "translation": "If you're that tired, you should rest early."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，明天我再去检查。",
                                        "pinyin": "",
                                        "translation": "Okay, I'll go for the check-up again tomorrow."
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
                        "title_zh": "如果……（的话），（S）就……",
                        "explanation": "This pattern is used to link a condition and its result in one sentence.",
                        "examples": [
                                {
                                        "zh": "如果你累了，就早点睡觉。",
                                        "pinyin": "",
                                        "meaning": "If you are tired, go to sleep early."
                                },
                                {
                                        "zh": "如果下雨的话，我们就不出去。",
                                        "pinyin": "",
                                        "meaning": "If it rains, we won't go out."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "复杂的状态补语",
                        "explanation": "This pattern describes the degree of an action or state in greater detail.",
                        "examples": [
                                {
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有累和睡觉。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 累 and 睡觉."
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
                                        "prompt": "tired",
                                        "answer": "累",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt": "to sleep",
                                        "answer": "睡觉",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt": "if",
                                        "answer": "如果",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt": "city",
                                        "answer": "城市",
                                        "pinyin": "chéngshì"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "累",
                                        "answer": "tired",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt": "睡觉",
                                        "answer": "to sleep",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt": "如果",
                                        "answer": "if",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt": "城市",
                                        "answer": "city",
                                        "pinyin": "chéngshì"
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
                                "累",
                                "睡觉",
                                "如果",
                                "城市"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "tired",
                                "to sleep",
                                "if",
                                "city"
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
                                "累",
                                "睡觉",
                                "如果"
                        ],
                        "example": "累 和 睡觉 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short text of 4-5 sentences about the lesson topic:",
                        "topic": "我现在累得下了班就想睡觉"
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
