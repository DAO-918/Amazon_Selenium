
data_dict= {
    'id': 1,
    'name': 'John',
    'age': 30,
    'city': None
    }
print(len(data_dict))
placeholders = ', '.join('?' * len(data_dict))
columns = ', '.join(data_dict.keys())
print(placeholders)
print(columns)