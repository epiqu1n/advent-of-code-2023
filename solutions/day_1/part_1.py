from resources.day_1_values import codes
import re

totalValue = 0
for code in codes:
  result = re.search('\d(.*\d)?', code)
  match = result.group()

  # Combine the first and last digit as strings, then convert to a number and add to the total value
  firstDigit = match[0]
  lastDigit = match[-1]
  combinedValue = int(firstDigit + lastDigit)
  totalValue += combinedValue

print(totalValue)
