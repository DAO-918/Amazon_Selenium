import time
import re
import requests
from random import randint
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from multiprocessing import Process
from PIL import Image
from io import BytesIO
import cv2
import numpy as np


def AMZInfo(
    valurl: str, isSmallImg: bool, isBigImg: bool, isKeepa: bool, is_Seller: bool
):  # sourcery skip: extract-method, hoist-statement-from-if, move-assign
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

    # 等待5秒,直到页面加载完成
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    actions = ActionChains(driver)

    if is_Seller:
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]')))
        seller_parent = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
        seller_Linechart = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[2]/div/div[1]/div[1]/div[2]/span')
        actions.move_to_element(seller_Linechart)
        actions.click(seller_Linechart)
        actions.perform()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')))
        seller_canvas = seller_parent.find_element(By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')
        seller_selector = seller_parent.find_element(By.CLASS_NAME,'rang-div')
        seller_selector_p = seller_selector.find_elements(By.TAG_NAME,'p')
        if seller_selector_p[-2].find_element(By.XPATH,'./span').text == '最近一年':
            actions.move_to_element(seller_selector_p[-2])
            actions.click(seller_selector_p[-2])
        else:
            actions.move_to_element(seller_selector_p[-1])
            actions.click(seller_selector_p[-1])
            actions.perform()

        '''
        location = seller_canvas.location
        size = seller_canvas.size
        # 获取截图范围
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        # 进行裁剪
        screenshot = Image.open(BytesIO("seller_canvas.png"))
        cropped_image = screenshot.crop((left, top, right, bottom))
        # 调整截图大小（可选）
        new_size = (300, 200)  # 设置新的大小，这里示例设置为宽度为300，高度为200
        cropped_image = cropped_image.resize(new_size)
        # 保存裁剪后的截图为seller_canvas_cropped.png
        cropped_image.save("seller_canvas_cropped.png")
        '''
        # //*[@id="seller-sprite-extension-quick-view-listing"]/div[1]
        ASIN = 'B0BHZDZHZM'
        seller_canvas.screenshot(f"D:\\AutoRPA\\卖家精灵\\{ASIN}\\seller_canvas.png")
        seller_quickiew = driver.find_element(By.XPATH,'//*[@id="seller-sprite-extension-quick-view-listing"]')
        # 获取元素的x,y坐标
        x = seller_quickiew.location['x']
        y = seller_quickiew.location['y']
        # 获取元素的宽高 
        width = seller_quickiew.size['width']
        height = seller_quickiew.size['height']
        # 滚动页面,使元素顶部与页面顶部对齐
        driver.execute_script(f"window.scrollTo(0, {y});")
        # 获取元素的x,y坐标
        x = seller_quickiew.location['x']
        y = seller_quickiew.location['y']
        # 截取指定区域
        driver.get_screenshot_as_file('screenshot.png')
        img = Image.open('screenshot.png')
        #img = img.crop((x, y, x+550, y+290)) 将元素顶部与页面顶部对齐后，y=0 img.crop((x, 0, x+550, 290)) 
        img = img.crop((x, 0, x+550, 290)) 
        img.save(f'D:\\AutoRPA\\卖家精灵\\{ASIN}\\seller_quickview.png')
        
        # 当发现截图只有一部分时，是该元素没有全部显示在页面中
        #seller_quickiew.screenshot(f'D:\\AutoRPA\\卖家精灵\\{ASIN}\\seller_quickview.png')


        '''
        # 读取元素模板图片，并转换为灰度图像
        # D:\Code\Amazon_Selenium\Resource\涓嬭浇.png
        # 文件路径中包含了中文字符，这可能导致了路径编码的错误,使用Python的原始字符串（Raw string）来表示文件路径
        template_path = r'D:\Code\Amazon_Selenium\Resource\download2.jpg'
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        #template = cv2.imread(template_path)

        # 检查是否成功读取模板图像
        if template is None:
            print(f"Failed to read the template image at path: {template_path}")
            exit()

        # 在网页中获取canvas截图
        canvas = driver.find_element(By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')
        canvas_screenshot = canvas.screenshot_as_png
        canvas_img = Image.open(BytesIO(canvas_screenshot)).convert('L')
        canvas_img_np = np.array(canvas_img)

        # 模板匹配
        res = cv2.matchTemplate(canvas_img_np, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 如果匹配值大于阈值,表示找到了匹配位置
        threshold = 0.8
        if max_val >= threshold:
            match_x = max_loc[0] + template.shape[1] // 2
            match_y = max_loc[1] + template.shape[0] // 2

            # 将匹配位置转换为 canvas 坐标点击
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(canvas, match_x, match_y).click().perform()
        else:
            print("No match found.")
        '''
        seller_container = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
        seller_logo = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[1]/div[1]/a/img')
        actions.move_to_element(seller_logo)
        #actions.click()
        actions.perform()
        location = seller_container.location
        size = seller_container.size
        print(location)
        print(size)
        actions = ActionChains(driver)
        #actions.move_to_element_with_offset(seller_container,100,10)
        actions.move_by_offset(1412, 180)
        #actions.context_click()
        actions.click()
        actions.perform()
        
    
    # 测试代码
if __name__ == '__main__':
    valurl1 = 'https://www.amazon.co.uk/dp/B0BHZDZHZM'
    print(AMZInfo(valurl1, True, True, False, True))
    # valurl2 = 'https://www.amazon.com/dp/B07B6NP36Q'
    # print(AmazonInfo.AMZInfo(valurl2,False,False,False))
    # valurl3 = 'https://www.amazon.com/dp/B09LY1LNGJ'
    # print(AmazonInfo.AMZInfo(valurl3,False,False,False))
    #valurl1 = 'https://www.amazon.co.uk/dp/B0BRN7HMDW?th=1'
    #print(AMZInfo(valurl1, True, True, False, True))
