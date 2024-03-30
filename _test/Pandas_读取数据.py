import configparser
import pandas as pd

# 读取配置文件
config = configparser.ConfigParser()
config_file_path = 'C:\\AutoRPA\\Config.ini'
with open(config_file_path, encoding='utf-8') as f:
    # 一直报错：configparser.NoSectionError: No section: 'Route'
    # 原因在于？？？
    # config.read(f)
    config.read_file(f)

# 获取文件路径配置信息
# file_route = config.get('File_Route', 'File_Route')
rpa_file_path = config.get('Route', 'RPAFilePath')
keyword_file_path = config.get('Route', 'KeywordFilePath')
kscore_file_path = config.get('Route', 'KScoreFilePath')
krank_file_path = config.get('Route', 'KRankFilePath')
kfre_file_path = config.get('Route', 'KFrequFilePath')
kcomp_file_path = config.get('Route', 'KCompFilePath')
history_file_path = config.get('Route', 'HistoryFilePath')
info_file_path = config.get('Route', 'InfoFilePath')
record_file_path = config.get('Route', 'RecordFilePath')
review_file_path = config.get('Route', 'ReviewFilePath')
arank_file_path = config.get('Route', 'ARankFilePath')
picture_file_path = config.get('Route', 'PictureFilePath')
ptrsc_file_path = config.get('Route', 'PtrscFilePath')
test_file_path = config.get('Route', 'TestFilePath')

# import xlrd
# wb_array = xlrd.open_workbook(info_file_path+'ASIN_Array_抓取队列.xlsx') 
# sheet_array = wb_array['Sheet1']
sheet_array_path = info_file_path+'ASIN_Array_抓取队列.xlsx'
sheet_info_path = info_file_path+'ASIN_Array_信息汇总.xlsx'
sheet_array = pd.read_excel(sheet_array_path, sheet_name='Sheet1')
sheet_info = pd.read_excel(sheet_info_path,sheet_name='Sheet1')

for index, row in sheet_array.iterrows():
    if index == 0:
        continue
    print(f'{str(index)}===={str(row)}')
    '''
    url = row[0]  # A列链接地址
    update = row[7]  # H列是否更新(布尔型)
    isSmallImg = row[8]  # I列主图450(布尔型)
    isBigImg = row[9]  # J列主图1200(布尔型)
    isKeepa = row[10]  # K列isKeepa(布尔型)
    isSeller = row[11]  # KL列isSeller(布尔型)
    print(f'url:{url}')
    print(f'update:{update}')
    print(f'isSmallImg:{isSmallImg}==isBigImg:{isBigImg}==isKeepa:{isKeepa}==isSeller:{isSeller}')
    url = row[0] if not pd.isna(url) else None
    update = row[7] if not pd.isna(update) else False
    isSmallImg = row[8] if not pd.isna(isSmallImg) else False
    isBigImg = row[9] if not pd.isna(isBigImg) else False
    isKeepa = row[10] if not pd.isna(isKeepa) else False
    isSeller = row[11] if not pd.isna(isSeller) else False
    print(f'url:{url}')
    print(f'update:{update}')
    print(f'isSmallImg:{isSmallImg}==isBigImg:{isBigImg}==isKeepa:{isKeepa}==isSeller:{isSeller}')
    '''
    url = None if pd.isna(row[0]) else row[0]
    update = False if pd.isna(row[7]) else row[7]
    isSmallImg = False if pd.isna(row[8]) else row[8]
    isBigImg = False if pd.isna(row[9]) else row[9]
    isKeepa = False if pd.isna(row[10]) else row[10]
    isSeller = False if pd.isna(row[11]) else row[11]
    print(f'url:{url}')
    print(f'update:{update}')
    print(f'isSmallImg:{isSmallImg}==isBigImg:{isBigImg}==isKeepa:{isKeepa}==isSeller:{isSeller}')