import re

'''text = '共140个产品1122'
numbers = re.findall(r'\d+',text )[0]
print(numbers)
numbers = re.findall(r'\d+',text )
print(numbers)

numbers = re.findall(r'\d+',text )
number = int(''.join(numbers))
print(number)

number = int(''.join(re.findall(r'\d+',text )))
print(number)'''


length = "8 x 3.5 x 10 inches"
length_list = re.findall(r'(\d+\.?\d*)', length)
length_list = [float(i) for i in length_list]
length_list.sort(reverse=True)
print(length_list)