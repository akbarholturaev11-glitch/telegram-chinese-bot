import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 13,
    "lesson_code": "HSK3-L13",
    "title": "我是走回来的",
    "goal": "expressing direction of movement and simultaneous actions",
    "intro_text": "This lesson is dedicated to expressing direction of movement and simultaneous actions. It uses 5 key vocabulary words and covers core grammar patterns such as 复合趋向补语 and 一边……一边……",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "礼物",
                        "pinyin": "lǐwù",
                        "pos": "n.",
                        "meaning": "gift, present"
                },
                {
                        "no": 2,
                        "zh": "奶奶",
                        "pinyin": "nǎinai",
                        "pos": "n.",
                        "meaning": "grandmother (paternal)"
                },
                {
                        "no": 3,
                        "zh": "遇到",
                        "pinyin": "yùdào",
                        "pos": "v.",
                        "meaning": "to run into, to meet"
                },
                {
                        "no": 4,
                        "zh": "一边",
                        "pinyin": "yìbiān",
                        "pos": "adv.",
                        "meaning": "at the same time, while"
                },
                {
                        "no": 5,
                        "zh": "愿意",
                        "pinyin": "yuànyì",
                        "pos": "v.",
                        "meaning": "to be willing to, to agree"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Walking back",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么回来的？",
                                        "pinyin": "",
                                        "translation": "How did you come back?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我是走回来的。",
                                        "pinyin": "",
                                        "translation": "I came back on foot."
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
                                        "zh": "路上你遇到谁了？",
                                        "pinyin": "",
                                        "translation": "Who did you run into on the way?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我一边走一边给奶奶买礼物。",
                                        "pinyin": "",
                                        "translation": "I walked back while buying a gift for my grandmother at the same time."
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
                        "title_zh": "复合趋向补语",
                        "explanation": "This topic shows the direction of movement of an action, or where the subject ends up as a result.",
                        "examples": [
                                {
                                        "zh": "我是走回来的。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有礼物和奶奶。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 礼物 and 奶奶."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "一边……一边……",
                        "explanation": "This pattern indicates that two actions are happening simultaneously.",
                        "examples": [
                                {
                                        "zh": "我一边走一边听音乐。",
                                        "pinyin": "",
                                        "meaning": "I listen to music while walking."
                                },
                                {
                                        "zh": "她一边做饭一边说话。",
                                        "pinyin": "",
                                        "meaning": "She talks while cooking."
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
                                        "prompt": "gift, present",
                                        "answer": "礼物",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt": "grandmother (paternal)",
                                        "answer": "奶奶",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt": "to run into, to meet",
                                        "answer": "遇到",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt": "at the same time, while",
                                        "answer": "一边",
                                        "pinyin": "yìbiān"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "礼物",
                                        "answer": "gift, present",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt": "奶奶",
                                        "answer": "grandmother (paternal)",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt": "遇到",
                                        "answer": "to run into, to meet",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt": "一边",
                                        "answer": "at the same time, while",
                                        "pinyin": "yìbiān"
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
                                "礼物",
                                "奶奶",
                                "遇到",
                                "一边"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "gift, present",
                                "grandmother (paternal)",
                                "to run into, to meet",
                                "at the same time, while"
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
                                "礼物",
                                "奶奶",
                                "遇到"
                        ],
                        "example": "礼物 和 奶奶 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "我是走回来的"
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
