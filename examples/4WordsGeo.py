# Encoding and decoding location in decimal degrees - can be used in new possible substitution of What3Words
# Their solution has problems in dictionary with ambiguously sound words and being proprietary -
# https://en.wikipedia.org/wiki/What3words
# Use of 4 short and simple words could work better - room for discussion

import src.word4num


def modification_to(string_number, adjustment, precise, decimal):
    string_number = str(round((float(string_number) + adjustment) / precise, decimal))
    while len(string_number.split('.')[1]) < decimal:
        string_number += '0'
    return string_number


def modification_from(string_number, adjustment, precise, decimal):
    string_number = str(round(float(string_number) * precise - adjustment, decimal))
    while len(string_number.split('.')[1]) < decimal:
        string_number += '0'
    return string_number


precise=5
decimal=5
words_base=5
latitude_converter = src.word4num.W4NConverter('199.'+'9'*decimal,
                                               'en',
                                               words_base,
                                               lambda x: modification_to(x, 90,precise,decimal),
                                               lambda x: modification_from(x, 90,precise,decimal))
longitude_converter = src.word4num.W4NConverter('399.'+'9'*decimal,
                                                'en',
                                                words_base,
                                                lambda x: modification_to(x, 180,precise,decimal),
                                                lambda x: modification_from(x, 180,precise,decimal))

test_location_gmap = '10.000000, 0.000001'
print(test_location_gmap)
result_location = ''
latitude, longitude = test_location_gmap.split(', ')

words_latitude = latitude_converter.encode_number(latitude)[0]
words_longitude = longitude_converter.encode_number(longitude)[0]

while len(words_latitude) < latitude_converter.words_number:
    words_latitude = [latitude_converter.num_to_word[0]] + words_latitude
while len(words_longitude) < longitude_converter.words_number:
    words_longitude = [longitude_converter.num_to_word[0]] + words_longitude
words = words_latitude + words_longitude
print(words)

decoded_latitude = latitude_converter.decode_words(words[:latitude_converter.words_number])
decoded_longitude = longitude_converter.decode_words(words[-longitude_converter.words_number:])
result_location = decoded_latitude + ', ' + decoded_longitude
print(result_location)
