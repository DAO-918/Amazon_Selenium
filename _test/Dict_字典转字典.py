import json
import ast

dict_Str = str({
    'Customer Reviews': '4.3\n181 ratings\n4.3 out of 5 stars',
    'Best Sellers Rank': '15,996 in Toys & Games (See Top 100 in Toys & Games)\n58 in Kites',
    'Date First Available': '23 Jun. 2020',
})

dict1=eval(dict_Str)
print('===============')
print(dict1['Best Sellers Rank'])

try: 
    dict2 = json.loads(dict_Str)
except json.decoder.JSONDecodeError as e:
    if dict_Str.startswith('{') and dict_Str.endswith('}'):
        # 如果是字典字符串,使用ast.literal_eval()解析
        d = ast.literal_eval(dict_Str)
    else:
        # 其他情况,抛出异常或进行其他处理
        raise ValueError('Invalid string format') from e
else:
    print('===============')
    print(dict2['Best Sellers Rank'])

dict3 = ast.literal_eval(dict_Str)
print('===============')
print(dict3['Best Sellers Rank'])