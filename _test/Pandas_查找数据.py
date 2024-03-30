import pandas as pd


sheet_array = pd.read_excel('D:\\AutoRPA\\产品信息\\'+'ASIN_Array_抓取队列.xlsx', sheet_name='Sheet1')
sheet_info = pd.read_excel('D:\\AutoRPA\\产品信息\\'+'ASIN_Array_信息汇总.xlsx',sheet_name='Sheet1')

first_col = sheet_array.iloc[:, 0] 
print('1===========================')
print(f'first_col:{first_col}')
'''
0    https://www.amazon.co.uk/dp/B08F9Y5RL9
1    https://www.amazon.co.uk/dp/B08TBVDWNV
2    https://www.amazon.co.uk/dp/B09XHLZSZ9
3    https://www.amazon.co.uk/dp/B087TYY7GB
4    https://www.amazon.co.uk/dp/B099JK9265
5    https://www.amazon.co.uk/dp/B09JP1FCNV
6    https://www.amazon.co.uk/dp/B0BS77QTTP
7    https://www.amazon.co.uk/dp/B0BRN7HMDW
8    https://www.amazon.co.uk/dp/B07CXVNFD5
Name: 链接, dtype: object
'''
findloc = sheet_array['链接'] == 'https://www.amazon.co.uk/dp/B0BRN7HMDW'
print('2===========================')
print(findloc)
'''
0    False
1    False
2    False
3    False
4    False
5    False
6    False
7     True
8    False
Name: 链接, dtype: bool
'''
findloc_data = sheet_array.loc[findloc]
print(findloc_data)

flag = sheet_array.loc[sheet_array['链接'] == 'https://www.amazon.co.uk/dp/B0BRN7HMDW'].index[0]
print('3===========================')
print(flag)
'''
7
'''

# 如果为空 IndexError: index 0 is out of bounds for axis 0 with size 0
try:
    flag = sheet_array.loc[sheet_array['链接'] == 'https://www.amazon.co.uk/dp/B078S'].index[0]
except IndexError:
    flag = False
    print('4===========================')

    print(flag)
else:
    print(flag)
    
print(flag)

flag = sheet_array.index[sheet_array['链接'] == 'https://www.amazon.co.uk/dp/B0BRN7HMDW'].tolist()
print('5===========================')
print(flag)

# first_col = sheet_array.iloc[:, 0]
# print(first_col)
'''
0    https://www.amazon.co.uk/dp/B08F9Y5RL9
1    https://www.amazon.co.uk/dp/B08TBVDWNV
2    https://www.amazon.co.uk/dp/B09XHLZSZ9
3    https://www.amazon.co.uk/dp/B087TYY7GB
4    https://www.amazon.co.uk/dp/B099JK9265
5    https://www.amazon.co.uk/dp/B09JP1FCNV
6    https://www.amazon.co.uk/dp/B0BS77QTTP
7    https://www.amazon.co.uk/dp/B0BRN7HMDW
8    https://www.amazon.co.uk/dp/B07CXVNFD5
Name: 链接, dtype: object
'''

# first_col 是一个 Pandas Series 对象,不能直接使用 in 运算符
# isExist = 'https://www.amazon.co.uk/dp/B0BRN7HMDW' in first_col
# isExist = 'https://www.amazon.co.uk/dp/B0BRN7HMDW' in first_col.isin()
# isExist = first_col.isin(['https://www.amazon.co.uk/dp/B0BRN7HMDW'])
# print(isExist)
'''
0    False
1    False
2    False
3    False
4    False
5    False
6    False
7     True
8    False
Name: 链接, dtype: bool
'''

# ERROR
# d:\Code\selenium_python\test\Pandas读取数据.py:63: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
# isExist_series = first_col.isin(['https://www.amazon.co.uk/dp/B0BRN7HMDW'])
# isExist = 'https://www.amazon.co.uk/dp/B0BRN7HMDW' in isExist_series.values
# print(isExist)


