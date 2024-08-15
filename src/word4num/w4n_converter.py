from .dicts import WordMap
from typing import Callable


class W4NConverter(WordMap):
    allowed_letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, number_mask: str, lang_symbol: str, words_base: int,
                 modification_to: Callable[[str], str] = lambda x: x,
                 modification_from: Callable[[str], str] = lambda x: x):
        super().__init__(lang_symbol, words_base)
        self.modification_to = modification_to
        self.modification_from = modification_from
        self.number_mask = number_mask
        self.max_number = self._find_max_number(number_mask)
        _, self.words_number = self.encode_number(self.modification_to(self.max_number))

    @staticmethod
    def _find_max_number(number_mask: str) -> str:
        max_text_number = ''
        for letter in number_mask:
            if letter == '#':
                max_text_number += '9'
            elif letter in W4NConverter.allowed_letters + ['.']:
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
        for character in range(len(self.number_mask)):
            reversed_character = -character - 1
            if self.number_mask[reversed_character] in W4NConverter.allowed_letters + ['#']:
                if (character < len(number_to_encode) and number_to_encode[reversed_character]
                        in W4NConverter.allowed_letters):
                    cleaned_number_to_encode = number_to_encode[reversed_character] + cleaned_number_to_encode
                else:
                    cleaned_number_to_encode = '0' + cleaned_number_to_encode

        return self._find_words_for_number(int(cleaned_number_to_encode))

    def decode_words(self, words_to_decode: list[str]) -> str:
        number = 0
        words_to_decode.reverse()
        for word in words_to_decode:
            number = number * self.get_map_length() + self.word_to_num[word]
        number = str(number)
        number_character = 0
        masked_number = ''
        for character in range(len(self.number_mask)):
            reversed_character = -character - 1
            if (number_character < len(number) and self.number_mask[reversed_character]
                    in W4NConverter.allowed_letters + ['#']):
                masked_number = number[-number_character - 1] + masked_number
                number_character += 1
            elif self.number_mask[reversed_character] in W4NConverter.allowed_letters + ['#']:
                masked_number = '0' + masked_number
            else:
                masked_number = self.number_mask[reversed_character] + masked_number
        return self.modification_from(masked_number)
