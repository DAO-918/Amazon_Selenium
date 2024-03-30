'''
import os

chrome_path = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
options = (
    '--remote-debugging-port=9222 --user-data-dir="D:\\Code\\selenium\\AutomationProfile"'
)
command = f'start {chrome_path} {options}'
os.system(command)
'''
import subprocess
import time
import re
import requests
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException 
from multiprocessing import Process

def OpenChrome():
    # 定义程序路径和参数
    program_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    program_args = [
        "--remote-debugging-port=9222",
        "--user-data-dir=D:/Code/selenium/AutomationProfile"
    ]
    # 使用 subprocess 执行外部命令
    subprocess.run([program_path] + program_args)
    return True

def OpenDriver(valurl: str):
    global driver
    # 绑定现有Chrome浏览器
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:9222'
    # timeout = 5  # 设置超时时间
    driver_exise = False
    while not driver_exise:
        error_occured = False
        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            # WebDriverException
            # print(f"An exception occurred: {e}")
            error_occured = True
        else:
            driver_exise = True
        if error_occured:
            # OpenChrome()
            # 使用进程代替线程,这可以更好地隔离进程内的问题,防止主进程被阻塞: 
            p = Process(target=OpenChrome)
            p.start()

    driver.maximize_window()
    # 打开新的标签页
    # driver.execute_script("window.open()") 通过执行JavaScript,在当前浏览器打开一个新的空白标签页。
    driver.execute_script("window.open()")
    # 切换到新标签页
    # driver.window_handles 获取所有的标签页handles,取最后一个就是最新标签页。
    driver.switch_to.window(driver.window_handles[-1])
    # 打开valurl网页
    try:
        driver.get(valurl)
    except Exception as e:
        for i in range(3):  # 重试3次
            try:
                driver = webdriver.Chrome(options=options)
                break
            except Exception:
                print(f'WebDriverException occurred, retrying {i+1} time')
                time.sleep(3)  # 等待3秒重试
    else:
        driver.get(valurl)
    # 等待5秒,直到页面加载完成
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    
    # 测试代码
if __name__ == '__main__':
    valurl1 = 'https://www.amazon.co.uk/HINAA-Pcs-Kids-Dinosaur-Toys/dp/B0BFXDTF7D'
    print(OpenDriver(valurl1))
