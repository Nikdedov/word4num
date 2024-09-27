# Encoding local telephone numbers in UK format into words
# Reasons:
# Words Carry Meaning: Words have meaning, context, and imagery associated with them, making them easier to remember.
# For example, words like "sun", "car", and "tree" evoke clear mental images or associations.
# Numbers Are Abstract: An 11-digit number like "12345678901" lacks inherent meaning and context,
# making it more difficult to recall without using specific memory techniques such as chunking or mnemonics.
# Chunking: The brain naturally chunks information for easier recall.
# While numbers can be chunked (e.g., phone numbers), it's generally easier for the brain to chunk and
# recall a few meaningful words than a long string of digits.

import src.word4num
import re

converter = src.word4num.W4NConverter('029########',
                                      'en',
                                      4,
                                      lambda x: re.sub(r'[^0-9+]', '', x))

test_phone = '(027) 4193 2856'
print(test_phone)
words = converter.encode_number(test_phone)
print(words)
result_phone = converter.decode_words(words[0])
print(result_phone)
