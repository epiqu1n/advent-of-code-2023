from resources.day_1_values import codes

number_words = { 'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9' }
number_words_regex = '|'.join(number_words.keys())

def word_is_number(word):
  return word in number_words

def word_to_digit(word):
  return number_words[word] if word in number_words else word

import re

total_value = 0
for code in codes:
  result = re.search(f'(?P<first_num>\d|{number_words_regex})(.*(?P<last_num>\d|{number_words_regex}))?', code)
  match_groups = result.groupdict()
  first_num = match_groups.get('first_num')
  last_num = match_groups.get('last_num') or first_num

  # Combine the first and last digit as strings, then convert to a number and add to the total value
  first_digit = word_to_digit(first_num)
  last_digit = word_to_digit(last_num)
  # print(f'{code}\n  ->{result.groupdict()}\n  -> first_digit: {first_digit}, last_digit: {last_digit}')
  combined_value = int(first_digit + last_digit)
  total_value += combined_value

print(total_value)

