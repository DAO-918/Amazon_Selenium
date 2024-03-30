import requests
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def AMZInfo(
    valurl: str, isSmallImg: bool, isBigImg: bool, isKeepa: bool, is_Seller: bool
):
    # 绑定现有Chrome浏览器
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:9222'
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()

    # 打开新的标签页
    # driver.execute_script("window.open()") 通过执行JavaScript,在当前浏览器打开一个新的空白标签页。
    driver.execute_script("window.open()")

    # 切换到新标签页
    # driver.window_handles 获取所有的标签页handles,取最后一个就是最新标签页。
    driver.switch_to.window(driver.window_handles[-1])

    # 打开valurl网页
    driver.get(valurl)

    '''
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
    '''

    # 等待5秒,直到页面加载完成
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    # 获取完整网页源码
    source = driver.page_source

    # 2.2 变体
    try:
        variant_element = driver.find_element(By.ID, 'twister_feature_div')
        variant_divs = variant_element.find_elements(By.XPATH, './/div[contains(@class, "twisterSwatchWrapper_0 twisterSwatchWrapper twisterImages thinWidthOverride")]')
        for variant_div in variant_divs:
            # ./ancestor::li[1] 来相对于 variant_div 元素查找最近的 li 父元素
            li_element = variant_div.find_element(By.XPATH,'./ancestor::li[1]')
            variant_ASIN = li_element.get_attribute('data-defaultasin')
            # 添加了一个.，表示相对于variant_div元素进行定位。这样可以确保XPath表达式在当前variant_div元素的上下文中执行，而不是全局执行。
            variant_img = variant_div.find_element(By.XPATH,'.//div[1]/img').get_attribute('src')
            variant_price = variant_div.find_element(By.XPATH,'.//div[2]/div/span/p').text
            print(f'variant_ASIN{variant_ASIN}====variant_img{variant_img}=====variant_price{variant_price}')
    except Exception:
        print('xx')
    else:
        count1= len(variant_divs)
        print(count1)
    
    
    # 测试代码
if __name__ == '__main__':
    # valurl1 = 'https://www.amazon.co.uk/dp/B0BHZDZHZM'
    # print(AMZInfo(valurl1, True, True, False, False))
    # valurl2 = 'https://www.amazon.com/dp/B07B6NP36Q'
    # print(AmazonInfo.AMZInfo(valurl2,False,False,False))
    # valurl3 = 'https://www.amazon.com/dp/B09LY1LNGJ'
    # print(AmazonInfo.AMZInfo(valurl3,False,False,False))
    valurl1 = 'https://www.amazon.co.uk/dp/B0BRN7HMDW?th=1'
    print(AMZInfo(valurl1, True, True, False, False))
