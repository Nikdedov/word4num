# Encoding and decoding location in decimal degrees - can be used in new possible substitution of What3Words
# Their solution has problems in dictionary with ambiguously sound words and being proprietary -
# https://en.wikipedia.org/wiki/What3words
# Use of 4 short and simple words could work better - room for discussion

import src.word4num


def modification_to(string_number, adjustment):
    string_number = str(round((float(string_number) + adjustment) / 3, 5))
    while len(string_number.split('.')[1]) < 5:
        string_number += '0'
    return string_number


def modification_from(string_number, adjustment):
    string_number = str(round(float(string_number) * 3 - adjustment, 5))
    while len(string_number.split('.')[1]) < 5:
        string_number += '0'
    return string_number


latitude_converter = src.word4num.W4NConverter('180.00000', 'en', 6, lambda x: modification_to(x, 90),
                                               lambda x: modification_from(x, 90))
longitude_converter = src.word4num.W4NConverter('360.00000', 'en', 6, lambda x: modification_to(x, 180),
                                                lambda x: modification_from(x, 180))

test_location_gmap = '51.488320, 0.002330'
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
decoded_latitude = latitude_converter.decode_words(words[:2])
decoded_longitude = longitude_converter.decode_words(words[-2:])
result_location = decoded_latitude + ', ' + decoded_longitude
print(result_location)
