import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 9,
    "lesson_code": "HSK3-L09",
    "title": "她的汉语说得跟中国人一样好",
    "goal": "expressing equality in degree through comparison",
    "intro_text": "This lesson is dedicated to expressing equality in degree through comparison. It introduces 5 key vocabulary words and covers core grammar patterns such as 越 A 越 B and 比较句 1：A 跟 B 一样 (+Adj).",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "中文",
                        "pinyin": "zhōngwén",
                        "pos": "n.",
                        "meaning": "Chinese language"
                },
                {
                        "no": 2,
                        "zh": "一样",
                        "pinyin": "yíyàng",
                        "pos": "adj.",
                        "meaning": "the same; alike"
                },
                {
                        "no": 3,
                        "zh": "参加",
                        "pinyin": "cānjiā",
                        "pos": "v.",
                        "meaning": "to participate; to join"
                },
                {
                        "no": 4,
                        "zh": "放心",
                        "pinyin": "fàngxīn",
                        "pos": "v.",
                        "meaning": "to feel at ease; to rest assured"
                },
                {
                        "no": 5,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "meaning": "to influence; influence / effect"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Language ability",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "translation": "She speaks Chinese just as well as a native Chinese person."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "是啊，所以大家都很放心。",
                                        "pinyin": "",
                                        "translation": "Yes, that's why everyone feels at ease."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Joining an event",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她会参加这次活动吗？",
                                        "pinyin": "",
                                        "translation": "Will she participate in this event?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "会，她的表现越说越自然。",
                                        "pinyin": "",
                                        "translation": "Yes, her speech is becoming more and more natural."
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
                        "title_zh": "越 A 越 B",
                        "explanation": "This grammar topic helps practice the core sentence patterns used in the lesson.",
                        "examples": [
                                {
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "meaning": "The key pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有中文和一样。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 中文 and 一样."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "比较句 1：A 跟 B 一样 (+Adj)",
                        "explanation": "This pattern is used to compare two things or people in terms of degree.",
                        "examples": [
                                {
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "meaning": "A comparison example from the lesson title."
                                },
                                {
                                        "zh": "中文比一样更重要。",
                                        "pinyin": "",
                                        "meaning": "中文 is even more important than 一样."
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
                                        "prompt": "Chinese language",
                                        "answer": "中文",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt": "the same; alike",
                                        "answer": "一样",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt": "to participate; to join",
                                        "answer": "参加",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt": "to feel at ease; to rest assured",
                                        "answer": "放心",
                                        "pinyin": "fàngxīn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "中文",
                                        "answer": "Chinese language",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt": "一样",
                                        "answer": "the same; alike",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt": "参加",
                                        "answer": "to participate; to join",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt": "放心",
                                        "answer": "to feel at ease; to rest assured",
                                        "pinyin": "fàngxīn"
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
                                "中文",
                                "一样",
                                "参加",
                                "放心"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "Chinese language",
                                "the same; alike",
                                "to participate; to join",
                                "to feel at ease; to rest assured"
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
                                "中文",
                                "一样",
                                "参加"
                        ],
                        "example": "中文 和 一样 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short passage of 4–5 sentences about the lesson topic:",
                        "topic": "她的汉语说得跟中国人一样好"
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
