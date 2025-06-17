import os

from aiogram.types import FSInputFile, Message

from src.db.database import db


async def send_congratulations(message: Message, user_id: str):
    photo_path_pattern = os.path.abspath("data/final_gift/")
    photo_path = os.path.join(photo_path_pattern, "Git - шпаркалка.png")
    photo = FSInputFile(photo_path)

    sum_mark = 0
    for i in range(1, 7):
        sum_mark += await db.get_test_mark(user_id, i)
    average_mark = round(sum_mark / 7, 2)

    text = (
        "🎉 <b>Поздравляем! Курс завершен. Ты Git-герой!</b> 🎉\n\n"
        f"Ты прошёл все <b>6 уроков</b> курса и твоя средняя оценка за тесты состовляет <b>{average_mark}%</b>.\n\n"
        "Каждый урок — шаг вперёд, теперь ты готов применять Git в проектах и командах. Спасибо, что был с нами!\n\n"
        "Удачи в новых проектах и помни: даже самый сложный конфликт можно разрешить!\n\n"
        "---\n\n"
        "🎁 <b>Твой бонус:</b> материал для закрепления знаний и шпаргалка с нужными командами.\n\n"
        "🔗 <a href=\"https://www.w3schools.com/git/default.asp\">W3Schools Git Tutorial</a> — больше теории и практики.\n"
        "🔗 <a href=\"https://githowto.com/ru\">Git How To</a> — интерактивный курс.\n"
        "🔗 <a href=\"https://www.geeksforgeeks.org/git-exercise/\">GeeksforGeeks Git Exercises</a> — дополнительная практика.\n"
        "🔗 <a href=\"https://learngitbranching.js.org/?locale=ru_RU\">Learn Git Branching</a> — основы и визуализация веток.\n"
        "🔗 <a href=\"https://git-scm.com/doc\">Документация Git</a>\n"
        "🔗 <a href=\"https://docs.github.com/ru/get-started/using-git/about-git\">Документация GitHub</a>"
    )

    await message.answer_photo(photo=photo, caption=text)
