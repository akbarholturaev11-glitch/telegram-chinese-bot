import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 4,
    "lesson_code": "HSK3-L04",
    "title": "她总是笑着跟客人说话",
    "goal": "expressing habitual actions and accompanying actions",
    "intro_text": "This lesson is dedicated to expressing habitual actions and accompanying actions. It uses 5 key vocabulary words and covers core grammar patterns such as 又……又…… and 动作的伴随：V1着(O1)+V2(O2).",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "总是",
                        "pinyin": "zǒngshì",
                        "pos": "adv.",
                        "meaning": "always"
                },
                {
                        "no": 2,
                        "zh": "客人",
                        "pinyin": "kèrén",
                        "pos": "n.",
                        "meaning": "guest, customer"
                },
                {
                        "no": 3,
                        "zh": "照片",
                        "pinyin": "zhàopiàn",
                        "pos": "n.",
                        "meaning": "photo, picture"
                },
                {
                        "no": 4,
                        "zh": "认真",
                        "pinyin": "rènzhēn",
                        "pos": "adj.",
                        "meaning": "serious, earnest"
                },
                {
                        "no": 5,
                        "zh": "蛋糕",
                        "pinyin": "dàngāo",
                        "pos": "n.",
                        "meaning": "cake"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "At the shop",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她总是笑着跟客人说话。",
                                        "pinyin": "",
                                        "translation": "She always smiles when talking to customers."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "对，她服务很认真。",
                                        "pinyin": "",
                                        "translation": "Yes, she provides very attentive service."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "At a party",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "桌子上又有蛋糕又有水果。",
                                        "pinyin": "",
                                        "translation": "There is both cake and fruit on the table."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我们先拍照片吧。",
                                        "pinyin": "",
                                        "translation": "Let's take a photo first."
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
                        "title_zh": "又……又……",
                        "explanation": "This pattern is used to emphasise two qualities or states simultaneously.",
                        "examples": [
                                {
                                        "zh": "这个蛋糕又甜又新鲜。",
                                        "pinyin": "",
                                        "meaning": "This cake is both sweet and fresh."
                                },
                                {
                                        "zh": "她又认真又热情。",
                                        "pinyin": "",
                                        "meaning": "She is both serious and warm."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "动作的伴随：V1着(O1)+V2(O2)",
                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "她总是笑着跟客人说话。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有总是和客人。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 总是 and 客人."
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
                                        "prompt": "always",
                                        "answer": "总是",
                                        "pinyin": "zǒngshì"
                                },
                                {
                                        "prompt": "guest, customer",
                                        "answer": "客人",
                                        "pinyin": "kèrén"
                                },
                                {
                                        "prompt": "photo, picture",
                                        "answer": "照片",
                                        "pinyin": "zhàopiàn"
                                },
                                {
                                        "prompt": "serious, earnest",
                                        "answer": "认真",
                                        "pinyin": "rènzhēn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "总是",
                                        "answer": "always",
                                        "pinyin": "zǒngshì"
                                },
                                {
                                        "prompt": "客人",
                                        "answer": "guest, customer",
                                        "pinyin": "kèrén"
                                },
                                {
                                        "prompt": "照片",
                                        "answer": "photo, picture",
                                        "pinyin": "zhàopiàn"
                                },
                                {
                                        "prompt": "认真",
                                        "answer": "serious, earnest",
                                        "pinyin": "rènzhēn"
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
                                "总是",
                                "客人",
                                "照片",
                                "认真"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "always",
                                "guest, customer",
                                "photo, picture",
                                "serious, earnest"
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
                                "总是",
                                "客人",
                                "照片"
                        ],
                        "example": "总是 和 客人 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "她总是笑着跟客人说话"
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
