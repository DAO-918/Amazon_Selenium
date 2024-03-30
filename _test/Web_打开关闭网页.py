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

valurl = 'https://www.amazon.co.uk/deals'
# 绑定现有Chrome浏览器
options = webdriver.ChromeOptions()
options.debugger_address = '127.0.0.1:9222'
driver = webdriver.Chrome(options=options)
# driver.maximize_window()

# 获取所有已打开页面的标签页
tabs = driver.window_handles

driver.execute_script("window.open('');") # 新建一个空白标签页
driver.switch_to.window(driver.window_handles[-1]) # 切换到新标签页  
driver.get(valurl) # 打开网址

print('do something')

driver.close() # 关闭当前标签页