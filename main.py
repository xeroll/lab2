"""Консольное меню для работы с номерами банковских карт."""

import requests

from card_regex import (
    find_cards_in_file,
    find_cards_in_url,
    get_payment_system,
    is_valid_card,
    normalize_card,
)


def print_menu():
    """Выводит меню программы."""
    print()
    print("1 - Проверить номер карты")
    print("2 - Найти номера карт в файле")
    print("3 - Найти номера карт на веб-странице")
    print("0 - Выход")


def print_cards(cards):
    """Выводит список найденных номеров карт."""
    if not cards:
        print("Номера карт не найдены.")
        return
    print("Найдено номеров:", len(cards))
    for card in cards:
        print(" ", card, "-", get_payment_system(card))


def check_card():
    """Проверяет номер карты, введённый пользователем."""
    card_number = input("Введите номер карты: ").strip()
    print()
    if is_valid_card(card_number):
        print("Номер корректен.")
        print("Платёжная система:", get_payment_system(card_number))
        print("Без разделителей:", normalize_card(card_number))
    else:
        print("Номер некорректен.")


def search_in_file():
    """Ищет номера карт в файле, путь к которому ввёл пользователь."""
    file_name = input("Введите путь к файлу: ").strip()
    try:
        cards = find_cards_in_file(file_name)
    except (OSError, UnicodeDecodeError) as error:
        print("Не удалось прочитать файл:", error)
        return
    print_cards(cards)


def search_in_url():
    """Ищет номера карт на веб-странице по адресу от пользователя."""
    url = input("Введите URL: ").strip()
    try:
        cards = find_cards_in_url(url)
    except requests.RequestException as error:
        print("Не удалось загрузить страницу:", error)
        return
    print_cards(cards)


def main():
    """Главный цикл программы."""
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            check_card()
        elif choice == "2":
            search_in_file()
        elif choice == "3":
            search_in_url()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
