def format_question_text(question_data: dict) -> str:
    """
    Форматирует текст вопроса с вариантами ответа.
    Пример результата:
    📌 1. Что такое Git?

    A) Программа для отслеживания финансовых транзакций
    B) Распределённая система управления версиями
    C) Локальный файловый менеджер
    D) Программа для хранения и шифрования данных
    """
    options_text = "\n".join(f"{letter}) {text}" for letter,
                             text in question_data["options"].items())
    return f"{question_data['question']}\n\n{options_text}"


def format_question_summary(question_data: dict, user_answer: str) -> str:
    """
    Форматирует итоговое сообщение с результатом ответа и отмеченными вариантами.
    Пример результата при верном ответе:
    Верно!
    📌 1. Что такое Git?
    A) Программа для отслеживания финансовых транзакций
    B) Распределённая система управления версиями ✅
    C) Локальный файловый менеджер
    D) Программа для хранения и шифрования данных
    """
    result_msg = "<b>Верно</b>" if user_answer == question_data["correct"] else "<b>Неверно</b>"
    marked_options = []
    for letter, text in question_data["options"].items():
        mark = "✅" if letter == question_data["correct"] else ""
        marked_options.append(f"{letter}) {text} {mark}")
    return f"{result_msg}\n\n{question_data['question']}\n" + "\n".join(marked_options)
