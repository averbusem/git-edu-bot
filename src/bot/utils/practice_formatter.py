def format_task_feedback(practice_data: dict, error_key: str) -> str:
    """
    Форматирует сообщение об ошибке и соответствующую подсказку для одного задания.
    """
    error_msg = practice_data.get("errors", {}).get(error_key, "❌ Неизвестная ошибка")
    hint = practice_data.get("hints", {}).get(error_key, "")
    if isinstance(hint, list):
        hint_text = "".join(hint)
    else:
        hint_text = hint
    return f"{error_msg}\n\n{hint_text}"


def get_practice_feedback(practice_data: dict, task_key: str, error_key: str) -> str:
    """
    Загружает JSON практики по её номеру, берёт из него нужное задание
    и возвращает отформатированный текст ошибки + подсказку.
    """
    task_data = practice_data.get("practices", {}).get(task_key)
    if not task_data:
        return "❌ Задание не найдено."

    return format_task_feedback(task_data, error_key)
