from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

options = webdriver.ChromeOptions() 
options.binary_location = r'D:\Code\chrome-win\chrome.exe'
options.debugger_address = '127.0.0.1:9222'
options.browser_version = '114.0.5734.0'
service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

print(type(driver))
print(type(webdriver.Chrome))

'''
<class 'selenium.webdriver.chrome.webdriver.WebDriver'>
<class 'abc.ABCMeta'>
driver变量是一个WebDriver类型的实例对象
webdriver.Chrome是一个类,而driver是通过调用该类创建出来的实例对象。
abc.ABCMeta是Python中用来标记抽象类的元类
'''

def get_title(driver:webdriver.Chrome):
    # 1. 标题、价格 获取//*[@id="expandTitleToggle"]、//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1] 中的文本
    title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
