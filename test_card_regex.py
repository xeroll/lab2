"""Unit-тесты для модуля card_regex."""

import unittest
from unittest.mock import patch

from card_regex import (
    find_cards,
    find_cards_in_file,
    find_cards_in_url,
    get_payment_system,
    is_valid_card,
    normalize_card,
)


class TestIsValidCard(unittest.TestCase):
    """Проверка одной строки: номер карты это или нет."""

    def test_valid_numbers(self):
        self.assertTrue(is_valid_card("4111111111111111"))
        self.assertTrue(is_valid_card("4111 1111 1111 1111"))
        self.assertTrue(is_valid_card("5555-5555-5555-4444"))
        self.assertTrue(is_valid_card("2200 1234 5678 9010"))

    def test_wrong_length(self):
        self.assertFalse(is_valid_card("411111111111111"))
        self.assertFalse(is_valid_card("41111111111111111"))

    def test_wrong_payment_system(self):
        self.assertFalse(is_valid_card("1234 5678 9012 3456"))
        self.assertFalse(is_valid_card("5600 0000 0000 0000"))
        self.assertFalse(is_valid_card("2205 0000 0000 0000"))

    def test_wrong_separators(self):
        self.assertFalse(is_valid_card("4111 1111-1111 1111"))
        self.assertFalse(is_valid_card("4111.1111.1111.1111"))

    def test_extra_text(self):
        self.assertFalse(is_valid_card("Карта 4111111111111111"))
        self.assertFalse(is_valid_card(""))


class TestFindCards(unittest.TestCase):
    """Поиск номеров карт в тексте."""

    def test_several_cards(self):
        text = "Карты: 4111111111111111 и 2200 1234 5678 9010."
        expected = ["4111111111111111", "2200 1234 5678 9010"]
        self.assertEqual(find_cards(text), expected)

    def test_no_cards(self):
        self.assertEqual(find_cards("Здесь нет номеров карт."), [])

    def test_part_of_long_number(self):
        # 20 цифр подряд - это не номер карты
        self.assertEqual(find_cards("41111111111111112222"), [])


class TestOtherFunctions(unittest.TestCase):
    """Вспомогательные функции."""

    def test_normalize_card(self):
        result = normalize_card("4111-1111-1111-1111")
        self.assertEqual(result, "4111111111111111")

    def test_payment_system(self):
        self.assertEqual(get_payment_system("4111111111111111"), "Visa")
        self.assertEqual(get_payment_system("5555555555554444"), "Mastercard")
        self.assertEqual(get_payment_system("2200123456789010"), "МИР")
        self.assertEqual(get_payment_system("1234"), "Неизвестно")


class TestSources(unittest.TestCase):
    """Поиск номеров карт в файле и на веб-странице."""

    def test_file(self):
        # В файле-примере 4 корректных номера
        cards = find_cards_in_file("cards_example.txt")
        self.assertEqual(len(cards), 4)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find_cards_in_file("no_such_file.txt")

    @patch("card_regex.requests.get")
    def test_url(self, mock_get):
        # Вместо настоящего запроса в интернет используется заглушка,
        # которая возвращает страницу с заданным текстом
        mock_get.return_value.text = "<p>4111-1111-1111-1111</p>"
        cards = find_cards_in_url("https://example.com")
        self.assertEqual(cards, ["4111-1111-1111-1111"])


if __name__ == "__main__":
    unittest.main()
