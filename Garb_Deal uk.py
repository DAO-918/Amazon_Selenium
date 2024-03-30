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
from Tools_RegEx import regex_ASIN, regex_Link
import datetime
import schedule
import pandas as pd
import sqlite3

# - 自动打开目标Amazon Deals页面
# - 循环遍历每一页的数据,提取每件商品的所需信息
# - 自动翻页,直到最后一页
# - 数据保存到Excel和SQLite本地数据库

def Garb_Dealinfo():
    # sourcery skip: hoist-statement-from-loop, remove-unnecessary-cast
    valurl = 'https://www.amazon.co.uk/deals'
    # 绑定现有Chrome浏览器
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:9222'
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()

    driver.execute_script("window.open('');")  # 新建一个空白标签页
    driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页
    driver.get(valurl)  # 打开网址

    time.sleep(2)
    toy_select_parent = driver.find_element(By.XPATH,'//*[@id="grid-main-container"]/div[2]')
    toy_select_spans = toy_select_parent.find_element(By.XPATH,'.//span[text()="Toys & Games"]')
    # sibling：当前元素节点的同级节点，结合preceding，following使用
    # preceding-sibling：当前元素节点之前的同级节点
    # following-sibling：当前元素节点之后的同级节点
    toy_select_input = toy_select_spans.find_element(By.XPATH,'./preceding-sibling::input')
    '''
    toy_select_input = driver.find_element(
        By.XPATH,
        '//*[@id="grid-main-container"]/div[2]/span[3]/ul/li[56]/label/input',
    )
    '''
    toy_select_input.click()

    data = []
    topic_deal = []
    columns = [
        'Link',
        'ASIN',
        'Country',
        'Image URL',
        'Title',
        'Discount',
        'Claimed',
        'Page',
        'Located',
        'Position',
        'Time',
        'isTop',
        'Topic',
        'price',
        'RRP',
    ]
    global_contry = ''
    global_link_f = ''

    while True:
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='grid-main-container']/div[3]/div")
            )
        )
        time.sleep(20)

        # 获取页码
        page_index = int(
            driver.find_element(
                By.XPATH,
                '//*[@id="dealsGridLinkAnchor"]/div/div[3]/div/ul/li[@class="a-selected"]/a',
            ).text
        )
        # 是否是最后一页
        page_next = driver.find_element(
            By.XPATH,
            '//*[@id="dealsGridLinkAnchor"]/div/div[3]/div/ul/li[contains(@class, "a-last")]',
        )
        isLastPage = False
        if "a-disabled" in page_next.get_attribute("class"):  # type: ignore
            isLastPage = True

        parent = driver.find_element(
            By.XPATH, '//*[@id="grid-main-container"]/div[3]/div'
        )
        divs = parent.find_elements(By.XPATH, './div')

        for located, div in enumerate(divs, start=1):
            try:
                position = (page_index - 1) * 60 + int(located)
                # 获取LINK ASIN //*[@id="grid-main-container"]/div[3]/div/div[57] /div/div/a
                #               //*[@id="grid-main-container"]/div[3]/div/div[1]
                link = div.find_element(By.XPATH, './div/div/a').get_attribute('href')
                if '/deal' in link or '/dp/' not in link:  # type: ignore
                    div_inner = div.find_element(By.XPATH, './div/div/a/div/div/img')
                    img_url = div_inner.get_attribute('data-a-hires')  # 或 src
                    title = div_inner.get_attribute('alt')
                    topic_deal.append((link, img_url, title, page_index, located, position))  # type: ignore
                    data.append(
                        (
                            link,
                            None,
                            None,
                            img_url,
                            title,
                            None,
                            None,
                            page_index,
                            located,
                            position,
                            datetime.datetime.now().strftime("%Y%m%d-%H:%M"),
                            True,
                            '',
                            0,
                            0,
                        )
                    )
                    continue

                link_dict = regex_ASIN(link)
                link = regex_Link(link_dict["ASIN"], link_dict["国家"])["链接"]
                # 获取图片地址 //*[@id="grid-main-container"]/div[3]/div/div[3] /div/div/a/div/div/img
                div_inner = div.find_element(By.XPATH, './div/div/a/div/div/img')
                img_url = div_inner.get_attribute('data-a-hires')  # 或 src
                # 获取标题
                title = div_inner.get_attribute('alt')
                # 获取Deal折扣
                discount = div.find_element(
                    By.XPATH, './div/div/div/span/div[1]/div'
                ).text.replace(' off', '')
                # 获取claimed进度
                claimed = None
                try:
                    claimed = div.find_element(
                        By.XPATH, './div/div/div/div/span/div/div[2]/span/div'
                    ).text.replace(' claimed', '')
                except Exception:
                    print('Not Found Claimed Bar')

                if int(page_index) == 1 and int(located) == 9:
                    global_contry = link_dict["国家"]
                    global_link_f = link[:-10]

                # columns=['Link','ASIN','Country','Image URL','Title', 'Discount', 'Claimed','Page','Located','Position','Time','IsTop']
                data.append(
                    (
                        link,
                        link_dict["ASIN"],
                        link_dict["国家"],
                        img_url,
                        title,
                        discount,
                        claimed,
                        page_index,
                        located,
                        position,
                        datetime.datetime.now().strftime("%Y%m%d-%H:%M"),
                        False,
                        '',
                        0,
                        0,
                    )
                )
                print(
                    f'第{page_index}页:\t第{located}个:\t{link_dict["ASIN"]}\t{discount}\t{claimed}'
                )
            except Exception as e:
                print('抓取错误')

        if isLastPage:
            break

        page_next.click()

    # 抓取结束
    driver.close()  # 关闭当前标签页
    '''
    # topic_deal (link, img_url, title, page_index, located, position)
    for topic in topic_deal:
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=options)
        driver.execute_script("window.open('');")  # 新建一个空白标签页
        driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页
        driver.get(topic[0])
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="octopus-dlp-asin-stream"]')
            )
        )
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="octopus-dlp-asin-stream"]/ul/li[1]/span/div/div[1]/a/img')
            )
        )
        time.sleep(10)
        
        isMultipage = False
        try:
            # //*[@id="octopus-dlp-pagination"]/div
            isMultipage = driver.find_element(
                By.XPATH, '//*[@id="octopus-dlp-pagination"]/div'
            )
        except Exception:
            isMultipage = False
        else:
            isMultipage = True
        while True:
            # //*[@id="octopus-dlp-asin-stream"]/ul
            parent = driver.find_element(
                By.XPATH, '//*[@id="octopus-dlp-asin-stream"]/ul'
            )
            lis = parent.find_elements(By.XPATH, './li')
            for located, li in enumerate(lis, start=1):
                # //*[@id="octopus-dlp-asin-stream"]/ul/li[1]/span/div/div[1]/a
                href = li.find_element(By.XPATH, './span/div/div[1]/a').get_attribute(
                    'href'
                )
                asin = ''
                asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
                match = asin_pattern.search(href)  # type: ignore
                asin = match[1] if match else None
                # //*[@id="octopus-dlp-asin-stream"]/ul/li[1]/span/div/div[1]/a/img
                title = li.find_element(
                    By.XPATH, './span/div/div[1]/a/img'
                ).get_attribute('alt')
                img_url = li.find_element(
                    By.XPATH, './span/div/div[1]/a/img'
                ).get_attribute('src')
                # //*[@id="octopus-dlp-asin-stream"]/ul/li[1]
                discount = (
                    li.find_element(
                        By.XPATH, './span/div/div[2]/div[3]/div/div[1]/span[1]'
                    ).text
                    + '%'
                )
                # //*[@id="octopus-dlp-asin-stream"]/ul/li[1]/span/div/div[2]/div[4]/span[1]/span[2]/span[2]
                # //*[@id="octopus-dlp-asin-stream"]/ul/li[25]/span/div/div[2]/div[4]/span[1]/span[2]/span[3]
                price_1 = li.find_element(
                    By.XPATH, './span/div/div[2]/div[4]/span[1]/span[2]/span[2]'
                ).text
                price_2 = li.find_element(
                    By.XPATH, './span/div/div[2]/div[4]/span[1]/span[2]/span[3]'
                ).text
                price = f'{price_1}.{price_2}'
                RRP = ''
                try:
                    # //*[@id="octopus-dlp-asin-stream"]/ul/li[25]/span/div/div[2]/div[4]/span[2]/span[2]
                    RRP = li.find_element(
                        By.XPATH, './span/div/div[2]/div[4]/span[2]/span[2]'
                    ).text
                except Exception:
                    try:
                        # //*[@id="octopus-dlp-asin-stream"]/ul/li[3]/span/div/div[2]/div[4]/span[3]/span[2]
                        RRP = li.find_element(
                            By.XPATH, './span/div/div[2]/div[4]/span[3]/span[2]'
                        ).text
                    except Exception:
                        RRP = ''
                data.append(
                    (
                        f'{global_link_f}{asin}',
                        asin,
                        global_contry,
                        img_url,
                        title,
                        discount,
                        None,
                        topic[3],
                        topic[4],
                        topic[5],
                        datetime.datetime.now().strftime("%Y%m%d-%H:%M"),
                        True,
                        topic[2],
                        price,
                        RRP,
                    )
                )

            class_context = ''
            page_next = ''
            try:
                # 获取页码 //*[@id="octopus-dlp-pagination"]/div/ul/li[2]/a
                page_index = int(
                    driver.find_element(
                        By.XPATH,
                        '//*[@id="octopus-dlp-pagination"]/div/ul/li[@class="a-selected"]/a',
                    ).text
                )
                # //*[@id="octopus-dlp-pagination"]/div/ul/li[5]
                page_next = driver.find_element(
                    By.XPATH,
                    '//*[@id="octopus-dlp-pagination"]/div/ul/li[contains(@class, "a-last")]',
                )
                page_next.get_attribute("class")
            except Exception:
                print(f'单页抓取：{topic[0]}')

            isLastPage = False
            if "a-disabled" in class_context:  # type: ignore
                driver.close()
                break

            if not isMultipage:
                driver.close()
                break

            page_next.click()  # type: ignore
    '''
    time_hour = datetime.datetime.now().strftime("%Y%m%d-%H")
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f'deals_data_{time_hour}.xlsx', index=False)

    conn = sqlite3.connect('deals.db')
    c = conn.cursor()
    # 创建数据表
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS deals (
            Link TEXT, 
            ASIN TEXT, 
            Country TEXT,
            Image_URL TEXT,
            Title TEXT, 
            Discount TEXT,
            Claimed TEXT,
            Page TEXT, 
            Located TEXT,  
            Position TEXT, 
            Time TEXT,
            IsTop BOOLEAN,
            Topic TEXT,
            Price REAL,     
            RRP REAL)      
    '''
    )
    # 插入多条数据
    c.executemany("INSERT INTO deals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()
    print("数据保存成功!")

'''
# 定义定时任务，每隔一小时执行一次
schedule.every(1).hours.do(Garb_Dealinfo)

# 循环运行调度器
while True:
    schedule.run_pending()
    # 每60秒钟运行一次，以确保调度器有足够的时间来检查是否有待运行的任务。
    time.sleep(1)
    print(f'{datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")}:等待执行')
'''

# 测试代码
if __name__ == '__main__':
    # 立即执行一次任务
    Garb_Dealinfo()

    while True:
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 当current_time.hour为23时，hour=current_time.hour + 1，hour为24，超出了0-23的范围
        if current_time.hour == 23:
            next_hour = current_time.replace(
                day=current_time.day + 1, hour=0, minute=0, second=0, microsecond=0
            )
        else:
            next_hour = current_time.replace(
                hour=current_time.hour + 1, minute=0, second=0, microsecond=0
            )
        # 计算距离下一个整点的时间差
        delta = next_hour - current_time
        seconds_to_wait = delta.total_seconds()
        # 等待到下一个整点时
        time.sleep(seconds_to_wait)
        Garb_Dealinfo()
