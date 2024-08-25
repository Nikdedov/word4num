# In my experience, remembering a postcode can take more than a few weeks

import src.word4num

converter_1part = src.word4num.W4NConverter('****',
                                            'en',
                                            6)
converter_2part = src.word4num.W4NConverter('#??',
                                            'en',
                                            6)

test_postcode = 'SE10 0TY'
print(test_postcode)
words = (converter_1part.encode_number(test_postcode.split(' ')[0])[0]
         + converter_2part.encode_number(test_postcode.split(' ')[1])[0])
print(words)
result_postcode = (converter_1part.decode_words(words[:2])
                   + ' ' + converter_2part.decode_words(words[2:]))
print(result_postcode)
