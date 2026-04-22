import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "a1",
    "lesson_order": 2,
    "lesson_code": "CEFR-A1-L02",
    "title": "Greetings and Introductions",
    "goal": "Learn how to greet people and introduce yourself in English.",
    "intro_text": "In this lesson we will learn common greetings and how to introduce yourself.",
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "hello",        "pinyin": "/həˈloʊ/",       "pos": "interj.", "meaning": "a common greeting"},
        {"no": 2,  "zh": "hi",           "pinyin": "/haɪ/",          "pos": "interj.", "meaning": "informal greeting, same as hello"},
        {"no": 3,  "zh": "good morning", "pinyin": "/ɡʊd ˈmɔːrnɪŋ/", "pos": "phrase", "meaning": "greeting used in the morning"},
        {"no": 4,  "zh": "good afternoon","pinyin": "/ɡʊd ˌæftərˈnuːn/","pos": "phrase","meaning": "greeting used in the afternoon"},
        {"no": 5,  "zh": "good evening", "pinyin": "/ɡʊd ˈiːvnɪŋ/", "pos": "phrase", "meaning": "greeting used in the evening"},
        {"no": 6,  "zh": "goodbye",      "pinyin": "/ˌɡʊdˈbaɪ/",    "pos": "interj.", "meaning": "said when leaving"},
        {"no": 7,  "zh": "bye",          "pinyin": "/baɪ/",          "pos": "interj.", "meaning": "informal way to say goodbye"},
        {"no": 8,  "zh": "my name is",   "pinyin": "/maɪ neɪm ɪz/",  "pos": "phrase", "meaning": "used to introduce yourself"},
        {"no": 9,  "zh": "nice to meet you", "pinyin": "/naɪs tə miːt juː/", "pos": "phrase", "meaning": "said when meeting someone for the first time"},
        {"no": 10, "zh": "how are you",  "pinyin": "/haʊ ɑːr juː/",  "pos": "phrase", "meaning": "asking about someone's wellbeing"},
        {"no": 11, "zh": "I am fine",    "pinyin": "/aɪ æm faɪn/",   "pos": "phrase", "meaning": "a positive answer to 'how are you'"},
        {"no": 12, "zh": "thank you",    "pinyin": "/θæŋk juː/",     "pos": "phrase", "meaning": "expressing gratitude"},
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Dialogue 1",
            "scene_label_zh": "First meeting",
            "dialogue": [
                {"speaker": "A", "zh": "Hello! My name is Tom.", "pinyin": "/həˈloʊ maɪ neɪm ɪz tɒm/"},
                {"speaker": "B", "zh": "Hi Tom! I am Sara. Nice to meet you.", "pinyin": "/haɪ tɒm aɪ æm ˈsærə naɪs tə miːt juː/"},
                {"speaker": "A", "zh": "Nice to meet you too, Sara.", "pinyin": "/naɪs tə miːt juː tuː ˈsærə/"},
                {"speaker": "B", "zh": "How are you?", "pinyin": "/haʊ ɑːr juː/"},
                {"speaker": "A", "zh": "I am fine, thank you. And you?", "pinyin": "/aɪ æm faɪn θæŋk juː ænd juː/"},
                {"speaker": "B", "zh": "I am fine too!", "pinyin": "/aɪ æm faɪn tuː/"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "Dialogue 2",
            "scene_label_zh": "Morning greeting",
            "dialogue": [
                {"speaker": "A", "zh": "Good morning, Maria!", "pinyin": "/ɡʊd ˈmɔːrnɪŋ məˈriːə/"},
                {"speaker": "B", "zh": "Good morning! How are you today?", "pinyin": "/ɡʊd ˈmɔːrnɪŋ haʊ ɑːr juː təˈdeɪ/"},
                {"speaker": "A", "zh": "I am great, thank you!", "pinyin": "/aɪ æm ɡreɪt θæŋk juː/"},
                {"speaker": "B", "zh": "Have a good day!", "pinyin": "/hæv ə ɡʊd deɪ/"},
                {"speaker": "A", "zh": "You too. Goodbye!", "pinyin": "/juː tuː ɡʊdˈbaɪ/"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "Dialogue 3",
            "scene_label_zh": "Evening farewell",
            "dialogue": [
                {"speaker": "A", "zh": "Good evening, John.", "pinyin": "/ɡʊd ˈiːvnɪŋ dʒɒn/"},
                {"speaker": "B", "zh": "Good evening! Are you leaving?", "pinyin": "/ɡʊd ˈiːvnɪŋ ɑːr juː ˈliːvɪŋ/"},
                {"speaker": "A", "zh": "Yes, goodbye. See you tomorrow!", "pinyin": "/jɛs ɡʊdˈbaɪ siː juː təˈmɒroʊ/"},
                {"speaker": "B", "zh": "Bye! See you!", "pinyin": "/baɪ siː juː/"},
            ]
        },
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "Formal vs informal greetings (Hello vs Hi)"},
        {"no": 2, "title_zh": "Time-based greetings: morning / afternoon / evening"},
        {"no": 3, "title_zh": "Introducing yourself: My name is... / I am..."},
        {"no": 4, "title_zh": "Responding to 'How are you?'"},
    ], ensure_ascii=False),
    "exercise_json": "[]",
    "answers_json": "[]",
    "homework_json": "[]",
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
