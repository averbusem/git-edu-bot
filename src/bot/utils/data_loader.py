import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_json(file_path: str) -> dict:
    """Читает JSON файл и возвращает словарь с данными"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_test_data(test_number: int) -> dict:
    """Загружает данные теста по его номеру"""
    file_name = f"test{test_number}.json"
    full_path = os.path.join(DATA_DIR, "tests", file_name)
    return load_json(full_path)


def get_theory_data(theory_number: int) -> dict:
    """Загружает данные урока теории по его номеру и объединяет части сообщений"""
    file_name = f"theory{theory_number}.json"
    full_path = os.path.join(DATA_DIR, "theories", file_name)
    data = load_json(full_path)

    messages = data.get("messages")
    if messages:
        for key in messages:
            if isinstance(messages[key], list):
                messages[key] = ''.join(messages[key])

    return data


def get_practice_data(practice_number: int) -> dict:
    """
    Загружает данные раздела практики по его номеру и рекурсивно объединяет
    все списки строк в единые строки.
    """
    file_name = f"practice{practice_number}.json"
    full_path = os.path.join(DATA_DIR, "tasks", file_name)
    data = load_json(full_path)

    def merge_lists(item, key=None):
        if isinstance(item, list) and all(isinstance(el, str) for el in item):
            if key == "expected":
                return item
            return "".join(item)
        if isinstance(item, list):
            return [merge_lists(el) for el in item]
        if isinstance(item, dict):
            return {k: merge_lists(v, k) for k, v in item.items()}

        return item

    return merge_lists(data)
