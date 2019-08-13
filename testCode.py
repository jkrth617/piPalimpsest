userInput = input('enter string: ')

onlyNumbers = []

def isNumber(char):
    return char.isdigit()

for char in userInput:
    if(isNumber(char)):
        onlyNumbers.append(char)
for num in onlyNumbers:
    print(num)

