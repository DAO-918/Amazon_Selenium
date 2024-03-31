import datetime
import time
import pandas as pd
from Grab_Info import AMZInfo
from Tools_Web import picdownload
from Tools_Execl import pdupdate
from Tools_Execl import pdformat
from Tools_Init import startInit
import re
import urllib.parse

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup

## ! 步骤二依次获取链接信息，存储到汇总

config = startInit()

sheet_array_path = config['info_file_path'] + 'ASIN_Array_抓取队列.xlsx'
sheet_info_path = config['info_file_path'] + 'ASIN_Array_信息汇总.xlsx'
sheet_array = pd.read_excel(sheet_array_path, sheet_name='Sheet1')
sheet_info = pd.read_excel(sheet_info_path, sheet_name='Sheet1')

#- 'int32','int64' - 整数型
#- 'float32','float64' - 浮点数型
#- 'str' - 字符串型
#- 'bool' - 布尔型
#- 'object' - 通用型
# DataFrame sheet_info的所有列的数据类型都转换为str
sheet_info = sheet_info.astype('object')
#for col in sheet_info.columns: #等同于
#    sheet_info[col] = sheet_info[col].astype('str')
#sheet_info['更新信息'] = sheet_info['更新信息'].astype(str)

options = webdriver.ChromeOptions()
options.binary_location = r'D:\Code\chrome-win\chrome.exe'
options.debugger_address = '127.0.0.1:9222'
options.browser_version = '114.0.5734.0'
#禁用Chrome浏览器的自动控制提示。当使用selenium开启Chrome浏览器时，浏览器的信息栏上方会有一条提示：“Chrome正在受到自动测试软件的控制”
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#禁用Selenium提供的自动化扩展。Selenium默认会载入一些用于自动化控制的浏览器扩展
#options.add_experimental_option('useAutomationExtension', False)
service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
#driver = webdriver.Chrome(service=service, options=options)设置超时时间20s，如果WebDriverException，
# 启动program_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# program_args = [
#        "--remote-debugging-port=9222",
#        "--user-data-dir=D:/Code/selenium/AutomationProfile",
#    ]的程序，且该程序只能存在一个

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.amazon.com")
us_cookies = driver.get_cookies()
driver.get("https://www.amazon.co.uk")
uk_cookies = driver.get_cookies()

driver.close

for index, row in sheet_array.iterrows():
    url = None if pd.isna(row['链接']) else row['链接']  # 链接地址
    updateTime = False if pd.isna(row['更新时间']) else row['更新时间']   # 是否更新(日期) # 45090 指 2023/6/13
    updateCycle = False if pd.isna(row['更新周期']) else int(row['更新周期'])  # 主图450(整数型)
    isUpdate = False if pd.isna(row['是否更新']) else bool(row['是否更新'])  # 是否更新(布尔型)
    isSmallImg = False if pd.isna(row['主图450']) else bool(row['主图450'])  # 主图450(布尔型)
    isBigImg = False if pd.isna(row['主图1500']) else bool(row['主图1500'])  # 主图1500(布尔型)
    isKeepa = False if pd.isna(row['isKeepa']) else bool(row['isKeepa'])  # isKeepa(布尔型)
    isSeller = False if pd.isna(row['isSeller']) else bool(row['isSeller'])  # isSeller(布尔型)
    
    ### 添加更新时间判断

    result = {}
    if url and isUpdate:
        result = AMZInfo(url, isSmallImg, isBigImg, isKeepa, isSeller)  # type: ignore
    else:
        continue

    if 'sspa' in url:
        asin_pattern = re.compile(r'dp%2F([A-Za-z0-9]{10})')
    else:
        asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
    match = asin_pattern.search(url)
    asin = match[1] if match else None
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    domain_parts = domain.split('.')
    if len(domain_parts) >= 4:
        domain_suffix = f'{domain_parts[-2]}.{domain_parts[-1]}'
    else:
        domain_suffix = domain_parts[-1]
    domain_suffix_country_dict = {'com': 'us', 'co.uk': 'uk'}
    country = domain_suffix_country_dict.get(domain_suffix, domain_suffix)
    new_url = f'https://{domain}/dp/{asin}'

    ASIN = result.get('ASIN')
    主图450 = result.get('主图450')
    主图1500 = result.get('主图1500')
    详情图片 = result.get('详情图片')
    picture_file_path = config['picture_file_path']
    image_dir = f'{picture_file_path}/{ASIN}/'
    if isSmallImg and 主图450 is not None:
        picdownload(us_cookies,uk_cookies,new_url,ASIN,country, 主图450, image_dir, '450')  # type: ignore[arg-type]
        #def picdownload(url, asin, country, img_list: list, image_dir, filename):


    #if isBigImg and 主图1500 is not None:
    #    picdownload(ASIN, 主图1500, image_dir, '1500')  # type: ignore[arg-type]

    #if 详情图片 is not None:
    #    picdownload(ASIN, 详情图片, image_dir, '详情')  # type: ignore[arg-type]

    pdupdate(sheet_info, result, sheet_info_path)
    
    time.sleep(5)

#sheet_info = pdformat(sheet_info)
sheet_info.to_excel(sheet_info_path, index=False)
