import json
from typing import Any


def _parse(value: Any, default: Any = None):
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return default


def _lang(item: dict, key: str, lang: str, fallback: str = "") -> str:
    return item.get(f"{key}_{lang}") or item.get(key) or fallback


def format_vocab(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    vocab = _parse(lesson.vocabulary_json, [])
    title = lesson.title or ""

    lines = []
    lines.append(f"【1/{lesson_total_steps}】 {title} · Yangi so'zlar 🇨🇳" if lang == "uz"
                 else f"【1/{lesson_total_steps}】 {title} · Калимаҳои нав 🇨🇳" if lang == "tj"
                 else f"【1/{lesson_total_steps}】 {title} · Новые слова 🇨🇳")
    lines.append("")

    intro_hint = {
        "uz": f"✨ Bugun {len(vocab)} ta so'z — darsni tugatgach ishlatishni bilasiz!",
        "tj": f"✨ Имрӯз {len(vocab)} калима — пас аз дарс истифода карда метавонед!",
        "ru": f"✨ Сегодня {len(vocab)} слов — после урока сможете их использовать!",
    }
    lines.append(intro_hint.get(lang, intro_hint["ru"]))
    lines.append("")

    nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, word in enumerate(vocab):
        if not isinstance(word, dict):
            continue
        zh = word.get("zh", "")
        pinyin = word.get("pinyin", "")
        meaning = word.get(lang) or word.get("meaning") or ""
        example_zh = word.get("example_zh", "")
        example_pinyin = word.get("example_pinyin", "")
        example_lang = word.get(f"example_{lang}") or word.get("example") or ""

        num = nums[i] if i < len(nums) else f"{i+1}."

        lines.append("━━━━━━━━━━━━━━")
        lines.append(f"{num}  {zh}")
        lines.append(f"     {pinyin}")
        lines.append(f"     👉 {meaning}")

        if example_zh:
            lines.append("")
            lines.append(f"     💬 {example_zh}")
            if example_pinyin:
                lines.append(f"        {example_pinyin}")
            if example_lang:
                lines.append(f"        {example_lang}")

        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    next_btn = {"uz": "▶️ Davom etish", "tj": "▶️ Идома додан", "ru": "▶️ Продолжить"}
    lines.append(next_btn.get(lang, next_btn["ru"]))

    return "\n".join(lines)


def format_dialogue(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    dialogues = _parse(lesson.dialogue_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Jonli dialog 🎭", "tj": "Муколамаи зинда 🎭", "ru": "Живой диалог 🎭"}
    lines = []
    lines.append(f"【2/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}")
    lines.append("")

    for block in dialogues:
        if not isinstance(block, dict):
            continue

        scene = block.get(f"scene_{lang}") or block.get("scene_uz") or ""
        if scene:
            lines.append(f"📍 {scene}")
            lines.append("")

        lines.append("━━━━━━━━━━━━━━")

        for line in block.get("lines", []):
            if not isinstance(line, dict):
                continue
            speaker = line.get("speaker", "")
            zh = line.get("zh", "")
            pinyin = line.get("pinyin", "")
            translation = line.get(lang) or line.get("uz") or ""

            icon = "👤" if speaker == "A" else "👥"
            lines.append(f"{icon} {speaker}:  {zh}")
            lines.append(f"       {pinyin}")
            lines.append(f"       {translation}")
            lines.append("")

        lines.append("━━━━━━━━━━━━━━")

        notes = block.get("notes", [])
        if notes:
            lines.append("")
            lines.append("💡 Bilasizmi?" if lang == "uz" else "💡 Медонед?" if lang == "tj" else "💡 Знаете ли вы?")
            for note in notes:
                note_text = note.get(lang) or note.get("uz") or ""
                if note_text:
                    lines.append(note_text)
        lines.append("")

    next_btn = {"uz": "▶️ Davom etish", "tj": "▶️ Идома додан", "ru": "▶️ Продолжить"}
    lines.append(next_btn.get(lang, next_btn["ru"]))

    return "\n".join(lines)


def format_grammar(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    grammar = _parse(lesson.grammar_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Grammatika 📐", "tj": "Грамматика 📐", "ru": "Грамматика 📐"}
    lines = []
    lines.append(f"【3/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}")
    lines.append("")

    for i, g in enumerate(grammar, 1):
        if not isinstance(g, dict):
            continue

        g_title = g.get(f"title_{lang}") or g.get("title_uz") or g.get("title_zh") or ""
        rule = g.get(f"rule_{lang}") or g.get(f"rule_uz") or ""

        lines.append("━━━━━━━━━━━━━━")
        lines.append(f"📌 {i}. {g_title}")
        lines.append("")
        if rule:
            for rule_line in rule.split("\n"):
                lines.append(f"   {rule_line}")
        lines.append("")

        examples = g.get("examples", [])
        if examples:
            eg_label = {"uz": "Misollar:", "tj": "Мисолҳо:", "ru": "Примеры:"}
            lines.append(f"   {eg_label.get(lang, eg_label['ru'])}")
            for ex in examples:
                zh = ex.get("zh", "")
                pinyin = ex.get("pinyin", "")
                meaning = ex.get(lang) or ex.get("uz") or ""
                lines.append(f"   • {zh} ({pinyin}) — {meaning}")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    next_btn = {"uz": "▶️ Davom etish", "tj": "▶️ Идома додан", "ru": "▶️ Продолжить"}
    lines.append(next_btn.get(lang, next_btn["ru"]))

    return "\n".join(lines)


def format_exercise(lesson, lang: str, exercise_index: int = 0, lesson_total_steps: int = 6) -> str:
    exercises = _parse(lesson.exercise_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Test vaqti! 🧠", "tj": "Вақти санҷиш! 🧠", "ru": "Время теста! 🧠"}
    lines = []
    lines.append(f"【5/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}")
    lines.append("")

    hint = {
        "uz": "Siz tayyor deb o'ylaymiz... Isbotlang! 😄",
        "tj": "Мо фикр мекунем шумо омодаед... Исбот кунед! 😄",
        "ru": "Думаем, вы готовы... Докажите! 😄",
    }
    lines.append(hint.get(lang, hint["ru"]))
    lines.append("")

    if exercise_index < len(exercises):
        ex = exercises[exercise_index]
        if isinstance(ex, dict):
            question = ex.get(f"question_{lang}") or ex.get("question_uz") or ""
            options = ex.get(f"options_{lang}") or ex.get("options_uz") or []

            lines.append("━━━━━━━━━━━━━━")
            lines.append(f"❓ {question}")
            lines.append("")
            for opt in options:
                lines.append(f"   {opt}")
            lines.append("━━━━━━━━━━━━━━")
            lines.append("")

            answer_hint = {"uz": "Javobingizni yozing ⬇️", "tj": "Посухатонро нависед ⬇️", "ru": "Напишите ответ ⬇️"}
            lines.append(answer_hint.get(lang, answer_hint["ru"]))

    return "\n".join(lines)


def format_intro(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    title = lesson.title or ""
    intro_raw = lesson.intro_text or ""

    try:
        intro_data = json.loads(intro_raw) if isinstance(intro_raw, str) else intro_raw
        intro = intro_data.get(lang) or intro_data.get("uz") or str(intro_data)
    except Exception:
        intro = intro_raw

    step_label = {"uz": "Darsga xush kelibsiz! 🎉", "tj": "Хуш омадед ба дарс! 🎉", "ru": "Добро пожаловать на урок! 🎉"}
    lines = []
    lines.append(f"【Dars {lesson.lesson_order}】 {title}")
    lines.append("")
    lines.append(step_label.get(lang, step_label["ru"]))
    lines.append("")
    lines.append("━━━━━━━━━━━━━━")
    lines.append(intro)
    lines.append("━━━━━━━━━━━━━━")
    lines.append("")

    start_btn = {"uz": "▶️ Boshlash", "tj": "▶️ Оғоз кардан", "ru": "▶️ Начать"}
    lines.append(start_btn.get(lang, start_btn["ru"]))

    return "\n".join(lines)
