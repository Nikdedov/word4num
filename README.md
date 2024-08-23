# word4num
Small library for encoding numbers to words and decoding it back. What can be encoded - any short code, phone number, decimal degrees geolocation, ip address etc.
Please share thoughts, ideas and suggestions and feel free to contact me.
## Installation
```sh
# install from PyPI
pip install word4num
```

## Idea
Define a unified mapping from number to words and promote single configuration for similar use cases that combination of words will work in the same way. 
For example: words combination generated in Google Maps will point to the same location in Apple Maps

## Usage
Simple use:
```python
import word4num
# initialise converter:
# '1###' - number mask, # - means that it could be any digit
# 'en' - language (English is only currently supported)
# 4 - max length of one word, could be up to 10
converter=word4num.W4NConverter('1###', 'en', 4)
words=converter.encode_number('1234')
print(converter.decode_words(words[0]))
```
Use with modifiers:
```python
import word4num
# initialise converters:
# '1####' - number mask, # - means that it could be any digit
# 'en' - language (English is only currently supported)
# 5 - max length of one word, could be up to 10
converter=word4num.W4NConverter('1####', 'en', 5)

# in case you don't need a precise number matching and length of words combination is more important
# could be used for decimal degrees geolocation
decreased_precision_converter=word4num.W4NConverter('1####', 'en', 5,lambda x: str(int(int(x)/5)),lambda x: str(int(x)*5) )

# encode same number using both converters
words=converter.encode_number('12344')
decreased_precision_words=decreased_precision_converter.encode_number('12344')

#compare length of words combination
print(len(words[0])>len(decreased_precision_words[0]))

# get decoded numbers
print(converter.decode_words(words[0]))
print(decreased_precision_converter.decode_words(decreased_precision_words[0]))
```

Other methods and available attributes:
```python
import word4num
# initialise converters:
# '1####' - number mask, # - means that it could be any digit
# 'en' - language (English is only currently supported)
# 5 - max length of one word, could be up to 10
converter=word4num.W4NConverter('1####', 'en', 5)

# configured mask
converter.number_mask

#maximum convertible number for configured converter
converter.max_number

#maximum number of words in combination - useful with converter.word_to_num when you want to combine several results of encoding
converter.words_number

#dictionaries of configured converter
converter.word_to_num
converter.num_to_word

#functions that were passed to the converter
converter.modification_to
converter.modification_from
#length of dictionary for configured converter
converter.get_map_length()
```
## Examples
1. examples/4WordsGeo.py :
    Encoding and decoding location in decimal degrees - can be used in new possible substitution of What3Words
    Their solution has problems in dictionary with ambiguously sound words and being proprietary - https://en.wikipedia.org/wiki/What3words
    Use of 4 short and simple words could work better - room for discussion

2. examples/LocalPhoneWords.py :
   Encoding local telephone numbers in UK format into words

3. examples/IntPhoneWords.py :
   Encoding international telephone numbers into words

Reasons for 2 and 3 example:
Words Carry Meaning: Words have meaning, context, and imagery associated with them, making them easier to remember. For example, words like "sun", "car", and "tree" evoke clear mental images or associations.
Numbers Are Abstract: An 11-digit number like "12345678901" lacks inherent meaning and context, making it more difficult to recall without using specific memory techniques such as chunking or mnemonics.
Chunking: The brain naturally chunks information for easier recall. While numbers can be chunked (e.g., phone numbers), it's generally easier for the brain to chunk and recall a few meaningful words than a long string of digits.

4. examples/IPv4toWords.py :
    Can be implemented as a simple local DNS for temporarily used IP addresses, JFF (e.g. web browser). Ports can be supported using 4 words.

## Words dictionary generation
1. English words were generated using NLTK using Brown Corpus.
2. Then stop words, proper names, plural words, abbreviations were filtered out to keep only nouns, verbs, adjectives, and adverbs.
3. Words frequencies were used to order list of words.
4. The resulting list was separated to 3,4,5,6,7,8,9,10 letters words to use shortest in some cases.

## TBD
1. Find out if support is needed for longer words
2. Support other languages
3. Add checks and exceptions
4. Add unit tests
5. 