import re

url1 = 'https://www.amazon.com/Dinosaur-Toys-Activity-Including-Triceratops/dp/B07TJSQF2J'
url2 = 'https://www.amazon.co.uk/HINAA-Pcs-Kids-Dinosaur-Toys/dp/B0BFXDTF7D?th=1'

# 编译正则表达式提取ASIN
asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')

# 从url1提取ASIN
match = asin_pattern.search(url1)
asin1 = match[1] if match else None  
print(f'ASIN1: {asin1}')

# 从url1提取国家代码 
country_code1 = url1.split('.')[2]
print(f'Country Code1: {country_code1}')

# 从url2提取ASIN  
match = asin_pattern.search(url2)
asin2 = match[1] if match else None  
print(f'ASIN2: {asin2}')

# 从url2提取国家代码
country_code2 = url2.split('/')[2].split('.')[-1]
print(f'Country Code2: {country_code2}')