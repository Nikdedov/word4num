class LetterMap:
    language_letters = {
        'en': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    }

    def __init__(self, lang_symbol: str):
        self.letter_number_map = {}
        self.number_letter_map = {}
        self.letters = LetterMap.language_letters[lang_symbol]
        self.max_letter_index = len(self.letters) - 1
        for letter_i in range(len(LetterMap.language_letters[lang_symbol])):
            self.letter_number_map[LetterMap.language_letters[lang_symbol][letter_i]] = letter_i
            self.number_letter_map[letter_i] = LetterMap.language_letters[lang_symbol][letter_i]

    def get_number(self, letter: str, mixed: bool = False) -> str:
        if letter.upper() not in self.letter_number_map.keys():
            number = letter
        else:
            shift = 10 if mixed else 0
            number = str(self.letter_number_map[letter.upper()] + shift)
        return number if len(number) > 1 else '0' + number

    def get_max_number(self, mixed: bool = False) -> str:
        if mixed:
            updated_max_letter_index = str(self.max_letter_index + 10)
        else:
            updated_max_letter_index = str(self.max_letter_index)
        return updated_max_letter_index[0] + '9' * (len(updated_max_letter_index) - 1)

    def get_letter(self, number: str, mixed: bool = False) -> str:
        if mixed:
            if int(number) < 10:
                return str(int(number))
            else:
                return self.number_letter_map[int(number) - 10]
        else:
            return self.number_letter_map[int(number)]
