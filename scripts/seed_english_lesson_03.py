import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "a1",
    "lesson_order": 3,
    "lesson_code": "CEFR-A1-L03",
    "title": "Numbers 1–10",
    "goal": "Learn to say and write the numbers 1 to 10 in English.",
    "intro_text": "In this lesson we will learn the numbers from one to ten and how to use them in sentences.",
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "one",   "pinyin": "/wʌn/",   "pos": "num.", "meaning": "the number 1"},
        {"no": 2,  "zh": "two",   "pinyin": "/tuː/",   "pos": "num.", "meaning": "the number 2"},
        {"no": 3,  "zh": "three", "pinyin": "/θriː/",  "pos": "num.", "meaning": "the number 3"},
        {"no": 4,  "zh": "four",  "pinyin": "/fɔːr/",  "pos": "num.", "meaning": "the number 4"},
        {"no": 5,  "zh": "five",  "pinyin": "/faɪv/",  "pos": "num.", "meaning": "the number 5"},
        {"no": 6,  "zh": "six",   "pinyin": "/sɪks/",  "pos": "num.", "meaning": "the number 6"},
        {"no": 7,  "zh": "seven", "pinyin": "/ˈsɛvən/","pos": "num.", "meaning": "the number 7"},
        {"no": 8,  "zh": "eight", "pinyin": "/eɪt/",   "pos": "num.", "meaning": "the number 8"},
        {"no": 9,  "zh": "nine",  "pinyin": "/naɪn/",  "pos": "num.", "meaning": "the number 9"},
        {"no": 10, "zh": "ten",   "pinyin": "/tɛn/",   "pos": "num.", "meaning": "the number 10"},
        {"no": 11, "zh": "how many", "pinyin": "/haʊ ˈmɛni/", "pos": "phrase", "meaning": "used to ask about a quantity"},
        {"no": 12, "zh": "there are", "pinyin": "/ðɛr ɑːr/", "pos": "phrase", "meaning": "used to say something exists or is present"},
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Dialogue 1",
            "scene_label_zh": "Counting objects",
            "dialogue": [
                {"speaker": "A", "zh": "How many apples are there?", "pinyin": "/haʊ ˈmɛni ˈæpəlz ɑːr ðɛr/"},
                {"speaker": "B", "zh": "There are five apples.", "pinyin": "/ðɛr ɑːr faɪv ˈæpəlz/"},
                {"speaker": "A", "zh": "And how many oranges?", "pinyin": "/ænd haʊ ˈmɛni ˈɒrɪndʒɪz/"},
                {"speaker": "B", "zh": "There are three oranges.", "pinyin": "/ðɛr ɑːr θriː ˈɒrɪndʒɪz/"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "Dialogue 2",
            "scene_label_zh": "In a shop",
            "dialogue": [
                {"speaker": "Customer", "zh": "I would like two coffees, please.", "pinyin": "/aɪ wʊd laɪk tuː ˈkɒfɪz pliːz/"},
                {"speaker": "Server",   "zh": "That is six dollars.", "pinyin": "/ðæt ɪz sɪks ˈdɒlərz/"},
                {"speaker": "Customer", "zh": "Here you go. Thank you.", "pinyin": "/hɪər juː ɡoʊ θæŋk juː/"},
                {"speaker": "Server",   "zh": "You are welcome!", "pinyin": "/juː ɑːr ˈwɛlkəm/"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "Dialogue 3",
            "scene_label_zh": "Giving a phone number",
            "dialogue": [
                {"speaker": "A", "zh": "What is your phone number?", "pinyin": "/wɒt ɪz jɔːr foʊn ˈnʌmbər/"},
                {"speaker": "B", "zh": "It is nine, four, seven, one, three.", "pinyin": "/ɪt ɪz naɪn fɔːr ˈsɛvən wʌn θriː/"},
                {"speaker": "A", "zh": "Let me write that down.", "pinyin": "/lɛt miː raɪt ðæt daʊn/"},
                {"speaker": "B", "zh": "Nine, four, seven, one, three. Got it?", "pinyin": "/naɪn fɔːr ˈsɛvən wʌn θriː ɡɒt ɪt/"},
                {"speaker": "A", "zh": "Yes, got it. Thank you!", "pinyin": "/jɛs ɡɒt ɪt θæŋk juː/"},
            ]
        },
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "Cardinal numbers: one, two, three ... ten"},
        {"no": 2, "title_zh": "Using 'there are' + number + noun"},
        {"no": 3, "title_zh": "Asking 'How many?' and answering with numbers"},
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
