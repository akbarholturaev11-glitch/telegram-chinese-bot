import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 11,
    "lesson_code": "HSK4-L11",
    "title": "读书好，读好书，好读书",
    "goal": "Talk about reading habits and methods; master grammar patterns 连……也/都……, 否则, 无论……都/也……, 然而, 同时",
    "intro_text": "This lesson is about the benefits of reading and how to develop good reading habits. You will learn how to talk about studying Chinese, taking exams, and the importance of reading widely. Key grammar patterns: 连……也/都……, 否则, 无论……都/也……, 然而, 同时.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "流利", "pinyin": "liúlì", "pos": "adj.", "meaning": "fluent"},
            {"no": 2, "zh": "厉害", "pinyin": "lìhai", "pos": "adj.", "meaning": "formidable, awesome, impressive"},
            {"no": 3, "zh": "语法", "pinyin": "yǔfǎ", "pos": "n.", "meaning": "grammar"},
            {"no": 4, "zh": "准确", "pinyin": "zhǔnquè", "pos": "adj.", "meaning": "accurate, precise"},
            {"no": 5, "zh": "词语", "pinyin": "cíyǔ", "pos": "n.", "meaning": "word, expression"},
            {"no": 6, "zh": "连", "pinyin": "lián", "pos": "prep./conj.", "meaning": "even (emphasizes extremes)"},
            {"no": 7, "zh": "阅读", "pinyin": "yuèdú", "pos": "v.", "meaning": "to read"},
            {"no": 8, "zh": "来得及", "pinyin": "láidejí", "pos": "v.", "meaning": "there is still time to do something"},
            {"no": 9, "zh": "复杂", "pinyin": "fùzá", "pos": "adj.", "meaning": "complicated, complex"},
            {"no": 10, "zh": "只好", "pinyin": "zhǐhǎo", "pos": "adv.", "meaning": "have no choice but to"},
            {"no": 11, "zh": "填空", "pinyin": "tián kòng", "pos": "v.", "meaning": "to fill in blanks"},
            {"no": 12, "zh": "猜", "pinyin": "cāi", "pos": "v.", "meaning": "to guess"},
            {"no": 13, "zh": "否则", "pinyin": "fǒuzé", "pos": "conj.", "meaning": "otherwise, or else"},
            {"no": 14, "zh": "客厅", "pinyin": "kètīng", "pos": "n.", "meaning": "living room"},
            {"no": 15, "zh": "无论", "pinyin": "wúlùn", "pos": "conj.", "meaning": "no matter, regardless of"},
            {"no": 16, "zh": "杂志", "pinyin": "zázhì", "pos": "n.", "meaning": "magazine"},
            {"no": 17, "zh": "著名", "pinyin": "zhùmíng", "pos": "adj.", "meaning": "famous, well-known"},
            {"no": 18, "zh": "页", "pinyin": "yè", "pos": "m.", "meaning": "page (measure word)"},
            {"no": 19, "zh": "增加", "pinyin": "zēngjiā", "pos": "v.", "meaning": "to increase, add"},
            {"no": 20, "zh": "文章", "pinyin": "wénzhāng", "pos": "n.", "meaning": "article, essay"},
            {"no": 21, "zh": "之", "pinyin": "zhī", "pos": "part.", "meaning": "classical connecting particle (of/between nouns)"},
            {"no": 22, "zh": "内容", "pinyin": "nèiróng", "pos": "n.", "meaning": "content"},
            {"no": 23, "zh": "然而", "pinyin": "rán'ér", "pos": "conj.", "meaning": "however, but (formal written)"},
            {"no": 24, "zh": "看法", "pinyin": "kànfǎ", "pos": "n.", "meaning": "viewpoint, opinion"},
            {"no": 25, "zh": "相同", "pinyin": "xiāngtóng", "pos": "adj.", "meaning": "same, identical"},
            {"no": 26, "zh": "顺序", "pinyin": "shùnxù", "pos": "n.", "meaning": "order, sequence"},
            {"no": 27, "zh": "表示", "pinyin": "biǎoshì", "pos": "v.", "meaning": "to express, indicate"},
            {"no": 28, "zh": "养成", "pinyin": "yǎngchéng", "pos": "v.", "meaning": "to form (a habit), develop"},
            {"no": 29, "zh": "同时", "pinyin": "tóngshí", "pos": "conj./adv.", "meaning": "at the same time, meanwhile"},
            {"no": 30, "zh": "精彩", "pinyin": "jīngcǎi", "pos": "adj.", "meaning": "wonderful, splendid"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "马克介绍自己学习汉语的方法",
                "dialogue": [
                    {"speaker": "老师", "zh": "马克，你的汉语说得这么流利，有什么好方法吗？", "pinyin": "", "translation": "Mark, your Chinese is so fluent — do you have any good methods?"},
                    {"speaker": "马克", "zh": "我每天都阅读中文文章，无论多忙，都坚持读至少十页。", "pinyin": "", "translation": "I read Chinese articles every day. No matter how busy I am, I always read at least ten pages."},
                    {"speaker": "老师", "zh": "那语法呢？语法对你来说复杂吗？", "pinyin": "", "translation": "What about grammar? Is grammar complicated for you?"},
                    {"speaker": "马克", "zh": "一开始连基本词语都不准确，然而通过大量阅读，我的语法慢慢提高了。", "pinyin": "", "translation": "At first I couldn't even get basic words right. However, through lots of reading, my grammar gradually improved."},
                    {"speaker": "老师", "zh": "你的方法很好！坚持阅读，同时注意语法，效果一定很好。", "pinyin": "", "translation": "Your method is great! Keeping up with reading while paying attention to grammar at the same time will definitely give good results."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "小夏和小雨聊考试情况",
                "dialogue": [
                    {"speaker": "小夏", "zh": "昨天的考试怎么样？", "pinyin": "", "translation": "How was yesterday's exam?"},
                    {"speaker": "小雨", "zh": "不太好。填空题太难了，连一半都没做对。", "pinyin": "", "translation": "Not great. The fill-in-the-blank questions were too hard — I couldn't even get half of them right."},
                    {"speaker": "小夏", "zh": "你平时有没有好好复习？否则考试的时候只好猜了。", "pinyin": "", "translation": "Did you study properly? Otherwise you have no choice but to guess during the exam."},
                    {"speaker": "小雨", "zh": "我知道，下次我一定要养成好的学习习惯，无论多累都要复习。", "pinyin": "", "translation": "I know. Next time I must develop good study habits — no matter how tired I am, I'll review my notes."},
                    {"speaker": "小夏", "zh": "对，来得及的话，我们一起学吧！", "pinyin": "", "translation": "Right! If there's still time, let's study together!"},
                ],
            },
            {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": "小李告诉小林阅读的好处",
                "dialogue": [
                    {"speaker": "小林", "zh": "你为什么每天都要看那么多杂志和书？", "pinyin": "", "translation": "Why do you read so many magazines and books every day?"},
                    {"speaker": "小李", "zh": "阅读能增加知识，同时让我的语言表达更加准确。", "pinyin": "", "translation": "Reading increases knowledge and at the same time makes my language expression more accurate."},
                    {"speaker": "小林", "zh": "那些著名文章的内容你都看懂了吗？", "pinyin": "", "translation": "Did you understand the content of those famous articles?"},
                    {"speaker": "小李", "zh": "大部分看懂了，然而有些词语还是不明白，只好查字典。", "pinyin": "", "translation": "I understood most of it. However, some words I still didn't understand, so I had no choice but to look them up in the dictionary."},
                    {"speaker": "小林", "zh": "精彩的书真的值得多读！我也要养成每天读书的习惯。", "pinyin": "", "translation": "Wonderful books are truly worth reading more! I also want to develop the habit of reading every day."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "连……也/都……",
                "explanation": "Means 'even'; used to emphasize an extreme or unexpected case. The element after 连 is what is surprising. Pattern: 连 + [noun/verb] + 也/都 + [predicate].",
                "examples": [
                    {"zh": "他连基本词语都不准确。", "pinyin": "", "meaning": "He can't even get basic words right."},
                    {"zh": "她忙得连饭都没时间吃。", "pinyin": "", "meaning": "She's so busy she doesn't even have time to eat."},
                ],
            },
            {
                "no": 2,
                "title_zh": "否则",
                "explanation": "Means 'otherwise, or else'; introduces a negative consequence that will happen if the preceding condition is not met. Used between two clauses.",
                "examples": [
                    {"zh": "你要好好复习，否则考试只好猜了。", "pinyin": "", "meaning": "You need to study well, otherwise you'll have no choice but to guess on the exam."},
                    {"zh": "快点走吧，否则要迟到了。", "pinyin": "", "meaning": "Hurry up, otherwise we'll be late."},
                ],
            },
            {
                "no": 3,
                "title_zh": "无论……都/也……",
                "explanation": "Means 'no matter what/how/who'; indicates that the result is the same regardless of the condition. Pattern: 无论 + [condition] + 都/也 + [result].",
                "examples": [
                    {"zh": "无论多忙，我都坚持阅读。", "pinyin": "", "meaning": "No matter how busy I am, I always keep reading."},
                    {"zh": "无论你去哪里，我都支持你。", "pinyin": "", "meaning": "No matter where you go, I will support you."},
                ],
            },
            {
                "no": 4,
                "title_zh": "然而",
                "explanation": "Means 'however, but'; a formal written conjunction that introduces a contrast or unexpected turn. Similar to 但是 but more literary.",
                "examples": [
                    {"zh": "我努力学习，然而成绩还是不理想。", "pinyin": "", "meaning": "I studied hard; however, my results were still not ideal."},
                    {"zh": "他看起来很轻松，然而内心很紧张。", "pinyin": "", "meaning": "He looked relaxed; however, he was very nervous inside."},
                ],
            },
            {
                "no": 5,
                "title_zh": "同时",
                "explanation": "Means 'at the same time, meanwhile'; indicates two actions or states occurring concurrently. Can also connect two parallel ideas.",
                "examples": [
                    {"zh": "阅读能增加知识，同时提高语言能力。", "pinyin": "", "meaning": "Reading increases knowledge and at the same time improves language ability."},
                    {"zh": "他是一位老师，同时也是一位作家。", "pinyin": "", "meaning": "He is a teacher, and at the same time also a writer."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "exercise_json": json.dumps(
        [
            {
                "no": 1,
                "type": "translate_to_chinese",
                "instruction": "Write the Chinese for the following words:",
                "items": [
                    {"prompt": "fluent", "answer": "流利", "pinyin": "liúlì"},
                    {"prompt": "grammar", "answer": "语法", "pinyin": "yǔfǎ"},
                    {"prompt": "accurate", "answer": "准确", "pinyin": "zhǔnquè"},
                    {"prompt": "article, essay", "answer": "文章", "pinyin": "wénzhāng"},
                    {"prompt": "to form a habit", "answer": "养成", "pinyin": "yǎngchéng"},
                    {"prompt": "wonderful, splendid", "answer": "精彩", "pinyin": "jīngcǎi"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_english",
                "instruction": "Write the English meaning of the following words:",
                "items": [
                    {"prompt": "词语", "answer": "word, expression", "pinyin": "cíyǔ"},
                    {"prompt": "增加", "answer": "to increase, add", "pinyin": "zēngjiā"},
                    {"prompt": "内容", "answer": "content", "pinyin": "nèiróng"},
                    {"prompt": "看法", "answer": "viewpoint, opinion", "pinyin": "kànfǎ"},
                    {"prompt": "顺序", "answer": "order, sequence", "pinyin": "shùnxù"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Choose the correct word to fill in the blank (连、否则、无论、然而、同时):",
                "items": [
                    {"prompt": "______多忙，我都坚持学习。", "answer": "无论", "pinyin": "wúlùn"},
                    {"prompt": "你要认真学习，______考试会不及格。", "answer": "否则", "pinyin": "fǒuzé"},
                    {"prompt": "他______基本的词语都不认识。", "answer": "连", "pinyin": "lián"},
                    {"prompt": "她努力工作，______照顾家庭。", "answer": "同时", "pinyin": "tóngshí"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["流利", "语法", "准确", "文章", "养成", "精彩"]},
            {"no": 2, "answers": ["word, expression", "to increase, add", "content", "viewpoint, opinion", "order, sequence"]},
            {"no": 3, "answers": ["无论", "否则", "连", "同时"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Write 3 sentences using the following words:",
                "words": ["流利", "养成", "阅读", "精彩"],
                "example": "我养成了每天阅读的好习惯，所以我的汉语越来越流利。",
            },
            {
                "no": 2,
                "instruction": "Write 2 sentences using the pattern '无论……都……'.",
                "topic": "about your study or daily life habits",
            },
            {
                "no": 3,
                "instruction": "Write a short paragraph of 5-6 sentences:",
                "topic": "What are the benefits of reading? 读书有哪些好处？",
            },
        ],
        ensure_ascii=False,
    ),
    "review_json": "[]",
    "is_active": True,
}


async def upsert_lesson():
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            for key, value in LESSON.items():
                setattr(existing, key, value)
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
