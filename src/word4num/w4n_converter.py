from .dicts import WordMap
from .letters import LetterMap
from typing import Callable


class W4NConverter(WordMap, LetterMap):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    special_symbols = ['#', '?', '*']

    def __init__(self, number_mask: str, lang_symbol: str, words_base: int,
                 modification_to: Callable[[str], str] = lambda x: x,
                 modification_from: Callable[[str], str] = lambda x: x):
        super().__init__(lang_symbol, words_base)
        super(WordMap, self).__init__(lang_symbol)
        self.modification_to = modification_to
        self.modification_from = modification_from
        self.number_mask = number_mask
        self.allowed_letters = W4NConverter.digits + self.letters
        self.max_number = self._find_max_number(number_mask)
        self.notation = self._generate_notation()
        _, self.words_number = self.encode_number(self.modification_to(self.max_number))

    def _find_max_number(self, number_mask: str) -> str:
        max_text_number = ''
        for letter in number_mask:
            if letter == '#':
                max_text_number += '9'
            elif letter == '?':
                max_text_number += self.get_max_number(False)
            elif letter == '*':
                max_text_number += self.get_max_number(True)
            elif letter.upper() in self.letters:
                max_text_number += self.get_number(letter, False)
            elif letter in W4NConverter.digits + ['.']:
                max_text_number += letter
        return max_text_number

    def _find_words_for_number(self, number: int) -> tuple[list[str], int]:
        words_number = 0
        result_words = []
        while number > self.get_map_length():
            number_remainder = number % self.get_map_length()
            result_words.append(self.num_to_word[number_remainder])
            number = (number - number_remainder) / self.get_map_length()
            words_number += 1
        else:
            result_words.append(self.num_to_word[number])
            words_number += 1
        return result_words, words_number

    def encode_number(self, number_to_encode: str) -> tuple[list[str], int]:
        number_to_encode = self.modification_to(number_to_encode)
        cleaned_number_to_encode = ''
        for character in range(min(len(self.number_mask), len(number_to_encode))):
            reversed_character = -character - 1
            if self.number_mask[reversed_character] in self.allowed_letters + W4NConverter.special_symbols:
                if number_to_encode[reversed_character] in self.allowed_letters:
                    if self.number_mask[reversed_character] == '*':
                        cleaned_number_to_encode = self.get_number(
                            number_to_encode[reversed_character],
                            True
                        ) + cleaned_number_to_encode
                    elif number_to_encode[reversed_character].upper() in self.letters:
                        cleaned_number_to_encode = self.get_number(
                            number_to_encode[reversed_character],
                            False
                        ) + cleaned_number_to_encode
                    else:
                        cleaned_number_to_encode = number_to_encode[reversed_character] + cleaned_number_to_encode

        return self._find_words_for_number(self._number_convert_to(cleaned_number_to_encode))

    def _find_number_for_words(self, words_to_decode: list[str]) -> int:
        number = 0
        skipped = 0
        for word_i in range(len(words_to_decode)):
            reversed_word_i = -word_i - 1
            if self.word_to_num[words_to_decode[reversed_word_i]] == 0:
                skipped += 1
            else:
                while skipped > 0:
                    number = number * self.get_map_length()
                    skipped -= 1
                number = number * self.get_map_length() + self.word_to_num[words_to_decode[reversed_word_i]]
        return number

    def decode_words(self, words_to_decode: list[str]) -> str:
        number = self._number_convert_from(self._find_number_for_words(words_to_decode))
        number_character = 0
        masked_number = ''
        for character in range(len(self.number_mask)):
            reversed_character = -character - 1
            if (
                    number_character < len(number) and
                    self.number_mask[reversed_character] in self.allowed_letters + W4NConverter.special_symbols
            ):
                if self.number_mask[reversed_character] in W4NConverter.digits + ['#']:
                    masked_number = number[-number_character - 1] + masked_number
                    number_character += 1
                else:
                    masked_number = self.get_letter(
                        number[-number_character - 2:-number_character if number_character != 0 else None],
                        self.number_mask[reversed_character] == '*'
                    ) + masked_number
                    number_character += 2
            elif self.number_mask[reversed_character] in W4NConverter.digits + ['#', '*']:
                masked_number = '0' + masked_number
            elif self.number_mask[reversed_character].upper() in self.letters + ['?']:
                masked_number = 'A' + masked_number
            else:
                masked_number = self.number_mask[reversed_character] + masked_number
        return self.modification_from(masked_number)

    def _generate_notation(self) -> list[int]:
        notation_list = [1]
        shift = 0
        for digit_i in range(len(self.max_number)):
            reversed_digit_i = -digit_i - 1
            if self.max_number[reversed_digit_i] in W4NConverter.digits:
                notation_list.insert(
                    0,
                    (int(self.max_number[reversed_digit_i]) + 1) * notation_list[reversed_digit_i + shift]
                )
            else:
                shift += 1
        return notation_list

    def _number_convert_to(self, number: str) -> int:
        result_number = 0
        for digit_i in range(len(number)):
            reversed_digit_i = -digit_i - 1
            result_number += int(number[reversed_digit_i]) * self.notation[reversed_digit_i]
        return result_number

    def _number_convert_from(self, number: int) -> str:
        result_number = ''
        for notation_i in self.notation:
            if number >= notation_i:
                number_remainder = number % notation_i
                result_number += str(int((number - number_remainder) / notation_i))
                number = number_remainder
            elif result_number != '':
                result_number += '0'
        return result_number
