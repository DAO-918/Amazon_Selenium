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
    '''
    # sourcery skip: hoist-statement-from-loop, remove-unnecessary-cast 是一个特殊的注释，用于 Sourcery 工具。Sourcery 是一个自动化代码优化工具，它可以分析代码并提供建议和自动化修复。在这个特定的注释中，hoist-statement-from-loop 和 remove-unnecessary-cast 是 Sourcery 提供的两种优化建议。
    hoist-statement-from-loop 意味着将循环中的语句提升到循环之外。这样可以减少循环内的重复计算或操作，提高代码效率。Sourcery 可能会根据代码分析提供将循环内部的语句移到循环外部的建议，并用这个注释来跳过 Sourcery 在这个地方的优化。
    remove-unnecessary-cast 意味着移除不必要的类型转换。有时代码中可能存在类型转换，但实际上转换是不必要的，因为变量已经是目标类型。Sourcery 可能会根据代码分析提供将不必要的类型转换移除的建议，并用这个注释来跳过 Sourcery 在这个地方的优化。
    在代码审查或代码优化过程中，Sourcery 可以自动分析并生成这样的优化建议，但有时也可能会出现误判。使用 # sourcery skip 注释可以告诉 Sourcery 在这个位置跳过对应的优化建议，避免对代码进行不必要的更改。
    '''
    valurl = 'https://www.amazon.com/deals'
    # 绑定现有Chrome浏览器
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:9222'
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()

    driver.execute_script("window.open('');")  # 新建一个空白标签页
    driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页
    driver.get(valurl)  # 打开网址

    time.sleep(2)
    # //*[@id="grid-main-container"]/div[2]
    toy_select_parent = driver.find_element(By.XPATH,'//*[@id="grid-main-container"]/div[2]')
    toy_select_spans = toy_select_parent.find_element(By.XPATH,'.//span[text()="Toys & Games"]')
    # sibling：当前元素节点的同级节点，结合preceding，following使用
    # preceding-sibling：当前元素节点之前的同级节点
    # following-sibling：当前元素节点之后的同级节点
    toy_select_input = toy_select_spans.find_element(By.XPATH,'./preceding-sibling::input')
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

        # 获取页码 //*[@id="dealsGridLinkAnchor"]/div/div[3]/div/ul/li[2]/a
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

        # //*[@id="grid-main-container"]/div[3]/div
        parent = driver.find_element(
            By.XPATH, '//*[@id="grid-main-container"]/div[3]/div'
        )
        divs = parent.find_elements(By.XPATH, './div')

        for located, div in enumerate(divs, start=1):
            try:
                position = (page_index - 1) * 60 + int(located)
                # 获取LINK ASIN //*[@id="grid-main-container"]/div[3]/div/div[57] /div/div/a
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
                # 获取Deal折扣 //*[@id="grid-main-container"]/div[3]/div/div[1] /div/div/div/span/div[1]/div
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

    time_hour = datetime.datetime.now().strftime("%Y%m%d-%H")
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f'deals_data_us_{time_hour}.xlsx', index=False)

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
                day=current_time.day + 1, hour=0, minute=30, second=0, microsecond=0
            )
        else:
            next_hour = current_time.replace(
                hour=current_time.hour + 1, minute=30, second=0, microsecond=0
            )
        # 计算距离下一个整点的时间差
        delta = next_hour - current_time
        seconds_to_wait = delta.total_seconds()
        # 等待到下一个整点时
        time.sleep(seconds_to_wait)
        Garb_Dealinfo()
