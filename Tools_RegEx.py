import re


def regex_ASIN(urlval):
    url_array = urlval.split('/')
    if url_array[3] != 'dp':
        ASIN = url_array[5][:10]
        urlval = f'{url_array[0]}//{url_array[2]}/{url_array[4]}/{ASIN}'
    else:
        ASIN = url_array[4][:10]
        urlval = f'{url_array[0]}//{url_array[2]}/{url_array[3]}/{ASIN}'
    '''
    # 编译正则表达式提取ASIN
    asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
    # 从url提取ASIN  
    match = asin_pattern.search(urlval)
    ASIN = match[1] if match else None
    print(f'ASIN: {ASIN}')
    '''
    # 从url提取国家代码
    Country = urlval.split('/')[2].split('.')[-1]
    print(f'Country: {Country}')

    if Country == 'com':
        Country = 'us'
    elif Country == 'co.uk':
        Country = 'uk'

    return {'链接': urlval, 'ASIN': ASIN, '国家': Country}


def regex_Link(ASIN, Country):
    if Country == 'us':
        urlval = f'https://www.amazon.com/dp/{ASIN}'
    elif Country == 'uk':
        urlval = f'https://www.amazon.co.uk/dp/{ASIN}'
    else:
        urlval = f'https://www.amazon.{Country}/dp/{ASIN}'
    return {'链接': urlval, 'ASIN': ASIN, '国家': Country}


# 测试代码
if __name__ == '__main__':
    valurl1 = 'https://www.amazon.com/dp/B09LY1LNGJ'
    valurl2 = 'https://www.amazon.co.uk/Control-Charging-Cartoon-Interactive-Birthday/dp/B0B5TNTQWY'
    print(valurl1.split('/'))
    print(valurl2.split('/'))
    print(regex_ASIN(valurl1))
    print(regex_ASIN(valurl2))
