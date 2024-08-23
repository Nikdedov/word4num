class LetterMap:
    language_letters={
        'en':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    }

    def __init__(self , lang_symbol : str):
        self.letter_number_map={}
        self.number_letter_map={}
        self.letters=language_letters[lang_symbol]
        self.max_letter_index=len(self.letters)-1
        for letter_i in range(len(language_letters[lang_symbol])):
            self.letter_number_map[language_letters[lang_symbol][letter_i]]=letter_i
            self.number_letter_map[letter_i]=language_letters[lang_symbol][letter_i]
    
    def get_number(self , letter : str) -> str:
        number=str(self.letter_number_map[letter.upper()])
        return number if len(number)>1 else '0'+number
    def get_letter(self , number : int) -> str:
        return self.number_letter_map[number]
