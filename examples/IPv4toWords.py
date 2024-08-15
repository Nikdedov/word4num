# can be implemented as simple local dns for temporarily used IP addresses, JFF (e.g. web browser)
# ports can be supported using 4 words

import src.word4num


def modification_to(string_number):
    list_of_numbers = string_number.split('.')
    for number in range(len(list_of_numbers)):
        while len(list_of_numbers[number]) < 3:
            list_of_numbers[number] = '0' + list_of_numbers[number]
    return '.'.join(list_of_numbers)


def modification_from(string_number):
    list_of_numbers = string_number.split('.')
    for number in range(len(list_of_numbers)):
        while list_of_numbers[number][0] == '0':
            list_of_numbers[number] = list_of_numbers[number][1:]
    return '.'.join(list_of_numbers)


converter = src.word4num.W4NConverter('255.255.255.255', 'en', 6, modification_to, modification_from)

test_ip = '92.132.10.22'

words = converter.encode_number(test_ip)
print(words)
result_ip = converter.decode_words(words[0])
print(result_ip)
