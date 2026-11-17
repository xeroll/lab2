"""
Проверка и поиск синтаксически корректных номеров банковских карт.

Какой номер считается корректным:
1. В номере ровно 16 цифр.
2. Номер начинается с цифр одной из платёжных систем:
   4            - Visa;
   51 - 55      - Mastercard;
   2200 - 2204  - МИР.
3. Номер записан слитно или группами по 4 цифры.
4. Группы разделены либо пробелами, либо дефисами
   (смешивать разные разделители нельзя).
"""

import re

import requests

FIRST_GROUP = r"(?:4\d{3}|5[1-5]\d{2}|220[0-4])"

# Три допустимых способа записи номера
WITHOUT_SEPARATORS = FIRST_GROUP + r"\d{12}"
WITH_SPACES = FIRST_GROUP + r" \d{4} \d{4} \d{4}"
WITH_HYPHENS = FIRST_GROUP + r"-\d{4}-\d{4}-\d{4}"

CARD_PATTERN = re.compile(
    r"\b(?:"
    + WITHOUT_SEPARATORS + "|" + WITH_SPACES + "|" + WITH_HYPHENS
    + r")\b"
)


def is_valid_card(card_number):
    """Проверяет, что вся строка целиком - корректный номер карты."""
    return CARD_PATTERN.fullmatch(card_number) is not None


def find_cards(text):
    """Возвращает список всех корректных номеров карт из текста."""
    return CARD_PATTERN.findall(text)


def normalize_card(card_number):
    """Убирает из номера карты пробелы и дефисы."""
    return re.sub(r"[ -]", "", card_number)


def get_payment_system(card_number):
    """Определяет платёжную систему по началу номера карты."""
    if not is_valid_card(card_number):
        return "Неизвестно"
    if card_number.startswith("4"):
        return "Visa"
    if card_number.startswith("5"):
        return "Mastercard"
    return "МИР"


def find_cards_in_file(file_name):
    """Читает текстовый файл и ищет в нём номера карт."""
    with open(file_name, encoding="utf-8") as file:
        text = file.read()
    return find_cards(text)


def find_cards_in_url(url):
    """Загружает веб-страницу по URL и ищет в ней номера карт."""
    response = requests.get(url, timeout=10)
    # Если сервер ответил кодом ошибки (4xx или 5xx), будет исключение
    response.raise_for_status()
    return find_cards(response.text)
