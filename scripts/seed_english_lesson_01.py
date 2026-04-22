import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "a1",
    "lesson_order": 1,
    "lesson_code": "CEFR-A1-L01",
    "title": "The English Alphabet and Sounds",
    "goal": "Learn the 26 letters of the English alphabet and their basic sounds.",
    "intro_text": "In this lesson we will learn the English alphabet — 26 letters, each with its own sound.",
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "vowel",     "pinyin": "/ˈvaʊəl/",     "pos": "n.", "meaning": "a speech sound made with an open mouth: A, E, I, O, U"},
        {"no": 2,  "zh": "consonant", "pinyin": "/ˈkɒnsənənt/", "pos": "n.", "meaning": "a speech sound that is not a vowel"},
        {"no": 3,  "zh": "alphabet",  "pinyin": "/ˈælfəbɛt/",   "pos": "n.", "meaning": "the set of letters used in a language"},
        {"no": 4,  "zh": "letter",    "pinyin": "/ˈlɛtər/",      "pos": "n.", "meaning": "a written symbol representing a sound"},
        {"no": 5,  "zh": "capital",   "pinyin": "/ˈkæpɪtəl/",   "pos": "adj.", "meaning": "uppercase letter — A, B, C"},
        {"no": 6,  "zh": "lowercase", "pinyin": "/ˈloʊərkeis/", "pos": "adj.", "meaning": "small letter — a, b, c"},
        {"no": 7,  "zh": "sound",     "pinyin": "/saʊnd/",       "pos": "n.", "meaning": "what you hear when you say a letter"},
        {"no": 8,  "zh": "spell",     "pinyin": "/spɛl/",        "pos": "v.", "meaning": "to write or say the letters of a word"},
        {"no": 9,  "zh": "pronounce", "pinyin": "/prəˈnaʊns/",   "pos": "v.", "meaning": "to make the sound of a word or letter"},
        {"no": 10, "zh": "word",      "pinyin": "/wɜːrd/",       "pos": "n.", "meaning": "a group of letters that means something"},
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Dialogue 1",
            "scene_label_zh": "In the classroom",
            "dialogue": [
                {"speaker": "Teacher", "zh": "Let's learn the alphabet today.", "pinyin": "/lɛts lɜːrn ðə ˈælfəbɛt təˈdeɪ/"},
                {"speaker": "Student", "zh": "How many letters are there?", "pinyin": "/haʊ ˈmɛni ˈlɛtərz ɑːr ðɛr/"},
                {"speaker": "Teacher", "zh": "There are 26 letters in English.", "pinyin": "/ðɛr ɑːr twɛntɪˈsɪks ˈlɛtərz ɪn ˈɪŋɡlɪʃ/"},
                {"speaker": "Student", "zh": "Are they all vowels?", "pinyin": "/ɑːr ðeɪ ɔːl ˈvaʊəlz/"},
                {"speaker": "Teacher", "zh": "No, there are 5 vowels: A, E, I, O, U.", "pinyin": "/noʊ ðɛr ɑːr faɪv ˈvaʊəlz/"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "Dialogue 2",
            "scene_label_zh": "Spelling a word",
            "dialogue": [
                {"speaker": "A", "zh": "How do you spell your name?", "pinyin": "/haʊ duː juː spɛl jɔːr neɪm/"},
                {"speaker": "B", "zh": "M-A-R-I-A. Maria.", "pinyin": "/ɛm eɪ ɑːr aɪ eɪ — məˈriːə/"},
                {"speaker": "A", "zh": "That is a beautiful name.", "pinyin": "/ðæt ɪz ə ˈbjuːtɪfəl neɪm/"},
                {"speaker": "B", "zh": "Thank you!", "pinyin": "/θæŋk juː/"},
            ]
        },
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "The 5 vowels: A, E, I, O, U"},
        {"no": 2, "title_zh": "Capital vs lowercase letters"},
        {"no": 3, "title_zh": "How to spell a word letter by letter"},
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
