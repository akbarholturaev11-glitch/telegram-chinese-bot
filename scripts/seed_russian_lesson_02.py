import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "russian1",
    "lesson_order": 2,
    "lesson_code": "RUS1-L02",
    "title": "Приветствия и знакомство",
    "goal": "Научиться здороваться, прощаться и представляться по-русски",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "ru": "Привет", "transcription": "Privet", "pos": "межд.", "meaning": "Hi / Hello (informal)"},
        {"no": 2, "ru": "Здравствуйте", "transcription": "Zdravstvuyte", "pos": "межд.", "meaning": "Hello (formal)"},
        {"no": 3, "ru": "Добрый день", "transcription": "Dobryy den", "pos": "фраза", "meaning": "Good afternoon"},
        {"no": 4, "ru": "Доброе утро", "transcription": "Dobroye utro", "pos": "фраза", "meaning": "Good morning"},
        {"no": 5, "ru": "Добрый вечер", "transcription": "Dobryy vecher", "pos": "фраза", "meaning": "Good evening"},
        {"no": 6, "ru": "До свидания", "transcription": "Do svidaniya", "pos": "фраза", "meaning": "Goodbye (formal)"},
        {"no": 7, "ru": "Пока", "transcription": "Paka", "pos": "межд.", "meaning": "Bye (informal)"},
        {"no": 8, "ru": "Как дела?", "transcription": "Kak dela?", "pos": "фраза", "meaning": "How are you?"},
        {"no": 9, "ru": "Хорошо", "transcription": "Khorosho", "pos": "нар.", "meaning": "Good / Fine"},
        {"no": 10, "ru": "Спасибо", "transcription": "Spasibo", "pos": "межд.", "meaning": "Thank you"},
        {"no": 11, "ru": "Пожалуйста", "transcription": "Pozhaluysta", "pos": "межд.", "meaning": "Please / You're welcome"},
        {"no": 12, "ru": "Меня зовут...", "transcription": "Menya zavut...", "pos": "фраза", "meaning": "My name is..."},
        {"no": 13, "ru": "Рад познакомиться", "transcription": "Rat paznakomitsya", "pos": "фраза", "meaning": "Nice to meet you"},
        {"no": 14, "ru": "Откуда вы?", "transcription": "Atkuda vy?", "pos": "фраза", "meaning": "Where are you from?"},
        {"no": 15, "ru": "Я из...", "transcription": "Ya iz...", "pos": "фраза", "meaning": "I am from..."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "Диалог 1",
            "scene_label_ru": "Первая встреча",
            "dialogue": [
                {"speaker": "А", "ru": "Привет! Как тебя зовут?", "transcription": "Privet! Kak tebya zavut?"},
                {"speaker": "Б", "ru": "Привет! Меня зовут Анна. А тебя?", "transcription": "Privet! Menya zavut Anna. A tebya?"},
                {"speaker": "А", "ru": "Меня зовут Алишер. Рад познакомиться!", "transcription": "Menya zavut Alisher. Rat paznakomitsya!"},
                {"speaker": "Б", "ru": "Очень приятно!", "transcription": "Ochen priyatna!"}
            ]
        },
        {
            "block_no": 2,
            "section_label": "Диалог 2",
            "scene_label_ru": "На работе",
            "dialogue": [
                {"speaker": "А", "ru": "Здравствуйте! Как вас зовут?", "transcription": "Zdravstvuyte! Kak vas zavut?"},
                {"speaker": "Б", "ru": "Здравствуйте! Меня зовут Иван Петров.", "transcription": "Zdravstvuyte! Menya zavut Ivan Petrov."},
                {"speaker": "А", "ru": "Откуда вы, Иван?", "transcription": "Atkuda vy, Ivan?"},
                {"speaker": "Б", "ru": "Я из Москвы. А вы?", "transcription": "Ya iz Moskvy. A vy?"},
                {"speaker": "А", "ru": "Я из Ташкента.", "transcription": "Ya iz Tashkenta."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "Диалог 3",
            "scene_label_ru": "Повседневное приветствие",
            "dialogue": [
                {"speaker": "А", "ru": "Доброе утро! Как дела?", "transcription": "Dobroye utro! Kak dela?"},
                {"speaker": "Б", "ru": "Доброе утро! Хорошо, спасибо. А у тебя?", "transcription": "Dobroye utro! Khorosho, spasibo. A u tebya?"},
                {"speaker": "А", "ru": "Тоже хорошо. Пока!", "transcription": "Tozhe khorosho. Paka!"},
                {"speaker": "Б", "ru": "До свидания!", "transcription": "Da svidaniya!"}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_ru": "Формальное и неформальное обращение (вы / ты)"},
        {"no": 2, "title_ru": "Конструкция «Меня зовут...» (My name is)"},
        {"no": 3, "title_ru": "Вопросительное слово «Как» (How / What)"}
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {"no": 1, "type": "fill", "instruction": "Заполните пропуск: _______ зовут Мария. (Меня / Тебя)"},
        {"no": 2, "type": "choose", "instruction": "Как правильно поздороваться утром? (Добрый вечер / Доброе утро)"},
        {"no": 3, "type": "translate", "instruction": "Переведите: How are you?"}
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answer": "Меня зовут Мария."},
        {"no": 2, "answer": "Доброе утро"},
        {"no": 3, "answer": "Как дела?"}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {"no": 1, "task": "Напишите небольшой диалог (4–6 строк) о знакомстве с новым человеком."}
    ], ensure_ascii=False),
    "review_json": json.dumps([
        {"no": 1, "question": "Как сказать 'Hello' формально?", "answer": "Здравствуйте"},
        {"no": 2, "question": "Как сказать 'My name is...'?", "answer": "Меня зовут..."},
        {"no": 3, "question": "Как сказать 'How are you?'?", "answer": "Как дела?"}
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
