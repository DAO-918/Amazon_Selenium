import time
import re
import requests
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

valurl = 'https://app.isellerpal.com/data/competing-products-query'
# 绑定现有Chrome浏览器
options = webdriver.ChromeOptions()
options.debugger_address = '127.0.0.1:9222'
driver = webdriver.Chrome(options=options)
# driver.maximize_window()

# 获取所有已打开页面的标签页
tabs = driver.window_handles

# 遍历标签页并获取对应页面网址
for tab in tabs:
    driver.switch_to.window(tab)
    url = driver.current_url
    if url == valurl:
        # 激活该标签页
        driver.switch_to.window(tab)
        print("切换到目标标签页")
        break

# 1. 初始化WebDriverWait,设置最长等待时间为5秒:
wait = WebDriverWait(driver, 20)
# 2. 使用until方法设置等待条件:
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

text = driver.find_element(
    By.XPATH, '//*[@id="isellerpal-main-box"]/div/div[2]/div[1]/div[1]/div[1]/span'
).text
ASIN_len = int(re.findall(r'\d+', text)[0])
# 执行向下滚动
body = driver.find_element(By.TAG_NAME, "body")
divs = []
running = True
while running:
    parent = driver.find_element(
        By.XPATH, '//*[@id="isellerpal-main-box"]/div/div[2]/div[1]/div[2]'
    )
    # By.XPATH, './div' 选取 parent 元素的直接子元素 div,返回 1 个元素
    # By.XPATH, './/div'选取parent元素下的所有div子孙元素,返回 n 个元素。
    # By.TAG_NAME, 'div' 指所有div元素
    divs = parent.find_elements(By.XPATH, './div')
    divs_len = len(divs)
    if ASIN_len != divs_len:
        body.send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_all_elements_located(divs[-1])) # type: ignore
    else:
        running = False

for div in divs:
    # 提取图片
    img_url = None
    try:
        img_url = div.find_element(By.CLASS_NAME, 'el-image__inner').get_attribute(
            'src'
        )
    except Exception:
        print('Not Found Image Element')
    # 提取ASIN
    asin = div.find_element(By.CLASS_NAME, 'goods-asin').text
    # 提取价格
    price = div.find_element(By.CLASS_NAME, 'goods-price').text
    # 提取销量
    #sold = (div.find_element(By.CLASS_NAME, 'el-popover__reference-wrapper').find_element(By.XPATH, './span').text)
    sold = div.find_element(By.XPATH, './/span[@class="related-msg el-popover__reference"]').text
    print(sold)
    # 提取标题
    title = div.find_element(By.CLASS_NAME, 'goods-introduce').text
    # 提取排名
    rank_items = div.find_elements(By.CLASS_NAME, 'rank-item')
    FRank = (
        rank_items[0].find_element(By.XPATH, './span[1]').text
        + rank_items[0].find_element(By.XPATH, './span[2]').text
    )
    SRank = (
        rank_items[1].find_element(By.XPATH, './span[1]').text
        + rank_items[1].find_element(By.XPATH, './span[2]').text
    )
    print(f'{img_url}=={asin}=={price}=={sold}=={title}=={FRank}=={SRank}')

    '''
    inner_div = div.find_element(By.XPATH, './div')
    inner_div_1 = inner_div.find_element(By.XPATH, './div[contains(@class, "flex")')
    inner_div_1_img = inner_div_1.find_element(By.XPATH, './div[contains(@class, "el-image goods-img")')
    img_url = None
    try:
        img_element = inner_div_1_img.find_element(By.TAG_NAME, 'img')
    except Exception:
        print('Not Found Image Element')
    else:
        img_url = img_element.get_attribute('src')

    inner_div_1_msg = inner_div_1.find_element(By.CLASS_NAME, 'goods-msg')
    ASIN = inner_div_1_msg.find_element(By.XPATH, '..//div[1]/div').text
    Price = inner_div_1_msg.find_element(By.XPATH, '..//div[2]/span').text
    Sold = inner_div_1_msg.find_element(By.XPATH, '..//div[4]/span').text

    inner_div_2 = inner_div.find_element(
        By.CLASS_NAME, 'goods-introduce text-text-gray-1'
    )
    Tittle = inner_div_2.text

    inner_div_3 = inner_div.find_element(By.CLASS_NAME, 'goods-rank')
    FRank = (
        inner_div_3.find_element(By.XPATH, '..//div[1]/span[1]').text
        + inner_div_3.find_element(By.XPATH, '..//div[1]/span[2]').text
    )
    SRank = (
        inner_div_3.find_element(By.XPATH, '..//div[2]/span[1]').text
        + inner_div_3.find_element(By.XPATH, '..//div[2]/span[2]').text
    )
    print(f'{img_url}=={ASIN}=={Price}=={Sold}=={Tittle}=={FRank}=={SRank}')
'''
