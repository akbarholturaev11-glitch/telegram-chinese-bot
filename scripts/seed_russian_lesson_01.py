import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "russian1",
    "lesson_order": 1,
    "lesson_code": "RUS1-L01",
    "title": "Русский алфавит",
    "goal": "Выучить буквы русского алфавита и научиться их произносить",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "ru": "А а", "transcription": "[a]", "pos": "буква"},
        {"no": 2, "ru": "Б б", "transcription": "[b]", "pos": "буква"},
        {"no": 3, "ru": "В в", "transcription": "[v]", "pos": "буква"},
        {"no": 4, "ru": "Г г", "transcription": "[g]", "pos": "буква"},
        {"no": 5, "ru": "Д д", "transcription": "[d]", "pos": "буква"},
        {"no": 6, "ru": "Е е", "transcription": "[ye]", "pos": "буква"},
        {"no": 7, "ru": "Ж ж", "transcription": "[zh]", "pos": "буква"},
        {"no": 8, "ru": "З з", "transcription": "[z]", "pos": "буква"},
        {"no": 9, "ru": "И и", "transcription": "[i]", "pos": "буква"},
        {"no": 10, "ru": "К к", "transcription": "[k]", "pos": "буква"},
        {"no": 11, "ru": "Л л", "transcription": "[l]", "pos": "буква"},
        {"no": 12, "ru": "М м", "transcription": "[m]", "pos": "буква"},
        {"no": 13, "ru": "Н н", "transcription": "[n]", "pos": "буква"},
        {"no": 14, "ru": "О о", "transcription": "[o]", "pos": "буква"},
        {"no": 15, "ru": "П п", "transcription": "[p]", "pos": "буква"},
        {"no": 16, "ru": "Р р", "transcription": "[r]", "pos": "буква"},
        {"no": 17, "ru": "С с", "transcription": "[s]", "pos": "буква"},
        {"no": 18, "ru": "Т т", "transcription": "[t]", "pos": "буква"},
        {"no": 19, "ru": "У у", "transcription": "[u]", "pos": "буква"},
        {"no": 20, "ru": "Ф ф", "transcription": "[f]", "pos": "буква"},
        {"no": 21, "ru": "Х х", "transcription": "[kh]", "pos": "буква"},
        {"no": 22, "ru": "Ц ц", "transcription": "[ts]", "pos": "буква"},
        {"no": 23, "ru": "Ч ч", "transcription": "[ch]", "pos": "буква"},
        {"no": 24, "ru": "Ш ш", "transcription": "[sh]", "pos": "буква"},
        {"no": 25, "ru": "Щ щ", "transcription": "[shch]", "pos": "буква"},
        {"no": 26, "ru": "Ъ ъ", "transcription": "[hard sign]", "pos": "буква"},
        {"no": 27, "ru": "Ы ы", "transcription": "[y]", "pos": "буква"},
        {"no": 28, "ru": "Ь ь", "transcription": "[soft sign]", "pos": "буква"},
        {"no": 29, "ru": "Э э", "transcription": "[e]", "pos": "буква"},
        {"no": 30, "ru": "Ю ю", "transcription": "[yu]", "pos": "буква"},
        {"no": 31, "ru": "Я я", "transcription": "[ya]", "pos": "буква"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Диалог 1",
            "scene_label_ru": "Знакомство с алфавитом",
            "dialogue": [
                {"speaker": "Учитель", "ru": "Посмотрите на алфавит. В русском языке 33 буквы.", "transcription": "Pasmatrite na alfavit. V russkom yazyke tridtsat tri bukvy."},
                {"speaker": "Ученик", "ru": "Это сложно?", "transcription": "Eta slozhna?"},
                {"speaker": "Учитель", "ru": "Нет, не сложно. Давайте начнём с гласных: А, Е, И, О, У.", "transcription": "Net, ne slozhna. Davajte nachnyom s glasnykh: A, Ye, I, O, U."},
                {"speaker": "Ученик", "ru": "Хорошо. А, Е, И, О, У.", "transcription": "Khorosho. A, Ye, I, O, U."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "Диалог 2",
            "scene_label_ru": "Практика произношения",
            "dialogue": [
                {"speaker": "Учитель", "ru": "Как произносится эта буква?", "transcription": "Kak proyznositsya eta bukva?"},
                {"speaker": "Ученик", "ru": "Это буква М. Она читается как [m].", "transcription": "Eta bukva M. Ana chitayetsya kak [m]."},
                {"speaker": "Учитель", "ru": "Правильно! Хорошо.", "transcription": "Pravilna! Khorosho."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_ru": "Гласные буквы: А, Е, Ё, И, О, У, Ы, Э, Ю, Я"},
        {"no": 2, "title_ru": "Согласные буквы и их произношение"},
        {"no": 3, "title_ru": "Твёрдый знак (Ъ) и мягкий знак (Ь)"}
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {"no": 1, "type": "read", "instruction": "Прочитайте вслух: А Б В Г Д Е Ж З И К"},
        {"no": 2, "type": "identify", "instruction": "Найдите гласные в слове: МАМА, ПАПА, ДОМА"}
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answer": "А Б В Г Д Е Ж З И К"},
        {"no": 2, "answer": "МАМА — А, А; ПАПА — А, А; ДОМА — О, А"}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {"no": 1, "task": "Напишите все 33 буквы русского алфавита по порядку."}
    ], ensure_ascii=False),
    "review_json": json.dumps([
        {"no": 1, "question": "Сколько букв в русском алфавите?", "answer": "33 буквы"},
        {"no": 2, "question": "Назовите 5 гласных букв.", "answer": "А, Е, И, О, У (и другие)"}
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
