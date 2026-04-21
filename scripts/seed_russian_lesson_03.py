import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "russian1",
    "lesson_order": 3,
    "lesson_code": "RUS1-L03",
    "title": "Числа от 1 до 10",
    "goal": "Научиться считать от 1 до 10 по-русски",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "ru": "один", "transcription": "adin", "pos": "числ.", "meaning": "one (1)"},
        {"no": 2, "ru": "два", "transcription": "dva", "pos": "числ.", "meaning": "two (2)"},
        {"no": 3, "ru": "три", "transcription": "tri", "pos": "числ.", "meaning": "three (3)"},
        {"no": 4, "ru": "четыре", "transcription": "chetyire", "pos": "числ.", "meaning": "four (4)"},
        {"no": 5, "ru": "пять", "transcription": "pyat", "pos": "числ.", "meaning": "five (5)"},
        {"no": 6, "ru": "шесть", "transcription": "shest", "pos": "числ.", "meaning": "six (6)"},
        {"no": 7, "ru": "семь", "transcription": "sem", "pos": "числ.", "meaning": "seven (7)"},
        {"no": 8, "ru": "восемь", "transcription": "vosem", "pos": "числ.", "meaning": "eight (8)"},
        {"no": 9, "ru": "девять", "transcription": "devyat", "pos": "числ.", "meaning": "nine (9)"},
        {"no": 10, "ru": "десять", "transcription": "desyat", "pos": "числ.", "meaning": "ten (10)"},
        {"no": 11, "ru": "сколько", "transcription": "skolka", "pos": "мест.", "meaning": "how many / how much"},
        {"no": 12, "ru": "номер", "transcription": "nomer", "pos": "сущ.", "meaning": "number"},
        {"no": 13, "ru": "телефон", "transcription": "telefon", "pos": "сущ.", "meaning": "phone"},
        {"no": 14, "ru": "лет", "transcription": "let", "pos": "сущ.", "meaning": "years (age)"},
        {"no": 15, "ru": "мне ... лет", "transcription": "mne ... let", "pos": "фраза", "meaning": "I am ... years old"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Диалог 1",
            "scene_label_ru": "В классе",
            "dialogue": [
                {"speaker": "Учитель", "ru": "Сколько студентов в классе?", "transcription": "Skolka studentav v klasse?"},
                {"speaker": "Ученик", "ru": "В классе восемь студентов.", "transcription": "V klasse vosem studentav."},
                {"speaker": "Учитель", "ru": "Хорошо! Посчитайте от одного до десяти.", "transcription": "Khorosho! Paschitayte at adnava da desyati."},
                {"speaker": "Ученик", "ru": "Один, два, три, четыре, пять, шесть, семь, восемь, девять, десять!", "transcription": "Adin, dva, tri, chetyire, pyat, shest, sem, vosem, devyat, desyat!"}
            ]
        },
        {
            "block_no": 2,
            "section_label": "Диалог 2",
            "scene_label_ru": "Обмен номерами",
            "dialogue": [
                {"speaker": "А", "ru": "Какой у тебя номер телефона?", "transcription": "Kakoy u tebya nomer telefona?"},
                {"speaker": "Б", "ru": "Мой номер: семь, восемь, девять...", "transcription": "Moy nomer: sem, vosem, devyat..."},
                {"speaker": "А", "ru": "Подожди, я запишу. Семь, восемь, девять...", "transcription": "Padazhdhi, ya zaprishu. Sem, vosem, devyat..."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "Диалог 3",
            "scene_label_ru": "Возраст",
            "dialogue": [
                {"speaker": "А", "ru": "Сколько тебе лет?", "transcription": "Skolka tebe let?"},
                {"speaker": "Б", "ru": "Мне пять лет.", "transcription": "Mne pyat let."},
                {"speaker": "А", "ru": "А мне семь лет.", "transcription": "A mne sem let."},
                {"speaker": "Б", "ru": "Ты старше меня!", "transcription": "Ty starshe menya!"}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_ru": "Числительные 1–10 и их произношение"},
        {"no": 2, "title_ru": "Конструкция «Мне ... лет» (I am ... years old)"},
        {"no": 3, "title_ru": "Вопрос «Сколько?» (How many?)"}
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {"no": 1, "type": "write", "instruction": "Напишите числа словами: 3, 7, 5, 10"},
        {"no": 2, "type": "translate", "instruction": "Переведите на русский: I am 8 years old."},
        {"no": 3, "type": "fill", "instruction": "Заполните: _______ студентов в классе? (используйте число 6)"}
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answer": "три, семь, пять, десять"},
        {"no": 2, "answer": "Мне восемь лет."},
        {"no": 3, "answer": "Шесть студентов в классе."}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {"no": 1, "task": "Составьте 3 предложения с числами от 1 до 10. Например: У меня три книги."}
    ], ensure_ascii=False),
    "review_json": json.dumps([
        {"no": 1, "question": "Как по-русски 'five'?", "answer": "пять"},
        {"no": 2, "question": "Как спросить возраст?", "answer": "Сколько тебе лет?"},
        {"no": 3, "question": "Как сказать 'I am 9 years old'?", "answer": "Мне девять лет."}
    ], ensure_ascii=False),
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
