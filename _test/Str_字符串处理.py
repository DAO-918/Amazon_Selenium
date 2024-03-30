data_dict = {
    'asin': 'B0C7H2SK2Z',
    'country': 'us',
    #'time': datetime.now().strftime("%Y-%m-%d"),
    'time': None,
    'image': 'https://m.media-amazon.com/images/I/91fSsBq-QUL._AC_UL320_.jpg',
    'title': 'JOYIN Dinosaur Truck for Kids with 6 Soft Rubber Dinosaur Car Vehicles, 1 Toy Dinosaur Transport Carrier Truck with Music and Roaring Sound, Flashing Lights, Mini Dinosaur Car Playset, Gift for Boys',
    'brand': 'JOYIN',
    'merchant_token': None}


placeholders = ', '.join("%s" * len(data_dict))
print(placeholders)
# %, s, %, s, %, s, %, s, %, s, %, s, %, s

placeholder = r'%s'
placeholders = ', '.join(placeholder * len(data_dict))
print(placeholders)

placeholder = r'%s, '
placeholders = ''
dict_len = len(data_dict)
for i in range(dict_len):
    placeholders = placeholders + placeholder
placeholders.strip(', ')
print(placeholders)


placeholders = []
for d in data_dict:
  placeholders.append('%s')

placeholders_str = ', '.join(placeholders)
print(placeholders_str)

