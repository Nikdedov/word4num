import json
import os


class WordMap:
    def __init__(self, lang_symbol: str, base: int):
        loader_i = 3
        self.word_to_num = {}
        self.num_to_word = {}
        word_iterator = 0
        while loader_i <= base:
            dictionary_file_name = str(loader_i) + '_' + lang_symbol + '_words.json'
            this_file = os.path.abspath(__file__)
            this_dir = os.path.dirname(this_file)
            dictionary_file_location = os.path.join(this_dir, dictionary_file_name)
            with open(dictionary_file_location, 'r') as json_file:
                # Step 3: Load the JSON data
                data = json.load(json_file)
                for word in data:
                    self.word_to_num[word] = word_iterator
                    self.num_to_word[word_iterator] = word
                    word_iterator += 1
            loader_i += 1

    def get_map_length(self) -> int:
        return len(self.word_to_num)
