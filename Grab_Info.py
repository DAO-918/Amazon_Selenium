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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions

from multiprocessing import Process
from PIL import Image
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import os

# 产品详情页抓取

def OpenChrome():
    # 定义程序路径和参数
    program_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    program_args = [
        "--remote-debugging-port=9222",
        "--user-data-dir=D:/Code/selenium/AutomationProfile",
    ]
    # 使用 subprocess 执行外部命令
    subprocess.run([program_path] + program_args)
    return True


def OpenDriver(valurl: str):
    global driver
    global wait
    # 绑定现有Chrome浏览器
    options = webdriver.ChromeOptions()
    # 屏蔽受控提示：正受到自动测试软件的控制
    #options.add_experimental_option('useAutomationExtension', False)
    # excludeSwitches 没有该参数，4.1可能修改这方面的写法
    #options.add_experimental_option("excludeSwitches", ['enable-automation'])
    
    # 加载用户默认数据
    # 如果发生以下错误selenium.common.exceptions.InvalidArgumentException: 
    # 指定目录已被占用，关闭所有浏览器窗口，重新发起浏览器会话即可；
    #user_conf = r'--user-data-dir="E:\Code\selenium\AutomationProfile 114"'
    #options.add_argument(user_conf)
    
    options.binary_location = r'D:\Code\chrome-win\chrome.exe'
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.debugger_address = '127.0.0.1:9222'
    options.browser_version = '114.0.5734.0'
    
    # 旧版本
    #chrome_driver_path = r'D:\Code\chromedriver_win32\114\chromedriver.exe'
    #driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options) # type: ignore
    # 4.1版本
    service = Service(executable_path=r'D:\Code\chromedriver_win32\114\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    # timeout = 5  # 设置超时时间
    '''driver_exise = False
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
            p.start()'''

    #driver.maximize_window()
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
    # 1. 初始化WebDriverWait,设置最长等待时间为5秒:
    wait = WebDriverWait(driver, 20)
    # 2. 使用until方法设置等待条件:
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    
    # expected_conditions检查网页元素是否可见
    #condition=expected_conditions.visibility_of_element_located((By.ID,'kw'))
    #WebDriverWait(driver=driver,timeout=20,poll_frequency=0.5).until(condition)
    #隐性等待，最长等待时间为30秒
    #driver.implicitly_wait(30)  


def AMZInfo(
    valurl: str, isSmallImg: bool, isBigImg: bool, is_Keepa: bool, is_Seller: bool
):
    OpenDriver(valurl)

    # 获取完整网页源码
    # source = driver.page_source
    # 打开文本文件并清空内容,将网页源码写入文本文件
    '''
    with open('page_source.txt', 'w', encoding='utf-8') as f:
        f.truncate()
        f.write(source)
    '''
    actions = ActionChains(driver)
    
    # 编译正则表达式提取ASIN
    asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
    # 从url1提取ASIN
    match = asin_pattern.search(valurl)
    ASIN = match[1] if match else None
    print(f'ASIN: {ASIN}')
    # 从url1提取国家代码
    Country = valurl.split('/')[2].split('.')[-1]
    if Country == 'com':
        Country = 'us'
    print(f'Country: {Country}')
    
    # 1. 标题、价格 获取//*[@id="expandTitleToggle"]、//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1] 中的文本
    isRefresh = True
    title = ''
    while isRefresh:
        try:
            title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
        except Exception:
            isRefresh = True
        else:
            isRefresh = False
        driver.refresh()
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
        time.sleep(20)  # Wait for 10 seconds before refreshing

        
    print(title)
    
    
    sale_price = None
    rrp_price = None
    is_Deal = False
    discount = None
    # 检查是否可售
    try:
        # 检查是否在Deal //*[@id="dealBadge_feature_div"]/span/span/span
        temp = driver.find_element(
            By.XPATH, '//*[@id="dealBadge_feature_div"]/span/span/span'
        ).text
        is_Deal = temp == 'Deal'
    except Exception:
        is_Deal = False

    prime_price = None
    try:
        prime_element = driver.find_element(
            By.XPATH, '//*[@id="pep-signup-link"]/span[2]'
        )
        prime_price = prime_element.text
    except Exception:
        print('No prime price element found')
    else:
        print(f'prime price : {prime_price}')

    isAvailable = False
    try:
        unavailable_element = driver.find_element(
            By.XPATH, '//*[@id="availability"]/span'
        )
        # 转化成小写
        unavailable_text = unavailable_element.text.lower()
        print(unavailable_text)
    except Exception:
        isAvailable = True
    else:
        if 'unavailable' in unavailable_text:
            sale_price = 'Unavailable'
            isAvailable = False
        elif 'stock' in unavailable_text:
            isAvailable = True

    if isAvailable:
        try:
            # 检查是否有折扣标识
            # apex_desktop 下两级 有的是 apex_desktop_newAccordionRow 有的是 apex_desktop_qualifiedBuybox
            apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
            corePrice_element = apex_element.find_element(
                By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]'
            )
            discount_element = corePrice_element.find_elements(
                By.XPATH,
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[contains(@class, "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")]',
            )[0]
            discount = discount_element.text
        except Exception:
            try:
                print('No discount info')
                # 无折扣,售价在第一个span
                # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]
                # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]
                apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
                sale_price_element = apex_element.find_element(
                    By.XPATH,
                    '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]',
                )
                driver.execute_script("arguments[0].className = ''; ", sale_price_element)
                sale_price = sale_price_element.text
            except Exception as e:
                print('=1=')
        else:
            if '%' in discount_element.text:
                try:
                    # 有折扣,售价在第二个span,原价在第四个span
                    sale_price_element = discount_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]',
                    )
                    # 删除class="a-offscreen"
                    driver.execute_script(
                        "arguments[0].className = ''; ", sale_price_element
                    )
                    # 再次获取text,此时可以获得正确值
                    sale_price = sale_price_element.text
                    #//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[1]
                    rrp_price_element = discount_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[1]',
                    )
                    driver.execute_script(
                        "arguments[0].className = ''; ", rrp_price_element
                    )
                    rrp_price = rrp_price_element.text
                except Exception as e:
                    print('=1=')
            else:
                try:
                    print('No discount info')
                    # 无折扣,售价在第一个span
                    apex_element = driver.find_element(By.XPATH, '//*[@id="apex_desktop"]')
                    sale_price_element = apex_element.find_element(
                        By.XPATH,
                        '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]',
                    )
                    driver.execute_script(
                        "arguments[0].className = ''; ", sale_price_element
                    )
                    sale_price = sale_price_element.text
                except Exception as e:
                    print('=1=')

        print(f'Is In Deal: {is_Deal}')
        print(f'Sale Price: {sale_price}')
        print(f'RRP Price: {rrp_price}') if rrp_price else print('No RRP Price')
        print(f'Discount off: {discount}')

    # 2. 评分、评论数 父元素//*[@id="averageCustomerReviews"],获取//*[@id="acrPopover"]/span[1]/a/span 文本,获取//*[@id="acrCustomerReviewText"]文本
    rating = ''
    review = ''
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="averageCustomerReviews"]')
        rating = parent.find_element(
            By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span'
        ).text

        review = parent.find_element(By.XPATH, '//*[@id="acrCustomerReviewText"]').text

    except Exception:
        print('No rating review element found')
    else:
        try:
            review = review.replace('ratings', '').strip()
        except Exception:
            print('')
        print(f'rating : {rating}')
        print(f'review : {review}')

    # 2.1 品牌获取//*[@id="bylineInfo"]的文本,并用空格分割字符串
    brand = ''
    try:
        brand = driver.find_element(By.ID, 'bylineInfo').text
        # 过滤字符串
        brand = brand.replace(':', '')  # 去除冒号
        brand = brand.replace('Visit the', '')  # 去除Visit the
        brand = brand.replace('Store', '')  # 去除Store
        brand = brand.replace('Brand', '')  # 去除Brand:
        brand = brand.strip()  # 去除首尾空格
        print(brand)
    except Exception:
        print('No brand element found')
    else:
        print(f'brand : {brand}')

    # 2.2 变体
    variant_info = []
    try:
        variant_element = driver.find_element(By.ID, 'twister_feature_div')
        variant_divs = variant_element.find_elements(
            By.XPATH,
            './/div[contains(@class, "twisterSwatchWrapper_0 twisterSwatchWrapper twisterImages thinWidthOverride")]',
        )
        for variant_div in variant_divs:
            # ./ancestor::li[1] 来相对于 variant_div 元素查找最近的 li 父元素
            li_element = variant_div.find_element(By.XPATH, './ancestor::li[1]')
            variant_ASIN = li_element.get_attribute('data-defaultasin')
            # 添加了一个.，表示相对于variant_div元素进行定位。这样可以确保XPath表达式在当前variant_div元素的上下文中执行，而不是全局执行。
            # variant_name = variant_div.find_element(By.XPATH,'.//div[1]/img').get_attribute('src')
            # variant_img = variant_div.find_element(By.XPATH,'.//div[1]/img').get_attribute('src')
            # variant_price = variant_div.find_element(By.XPATH,'.//div[2]/div/span/p').text
            variant_name = ''
            try:
                variant_name = variant_div.find_element(
                    By.XPATH, './/div[contains(@class, "twisterTextDiv")]//p[last()]'
                ).text
            except Exception:
                print('No variant_name found')
            variant_img = ''
            try:
                variant_img = variant_div.find_element(
                    By.XPATH, './/div[contains(@class, "twisterImageDiv")]//img[last()]'
                ).get_attribute('src')
            except Exception:
                print('No variant_img found')
            variant_price = variant_div.find_element(
                By.XPATH, './/div[contains(@class, "twisterSlotDiv")]//p[last()]'
            ).text
            print(
                f'variant_ASIN:{variant_ASIN}====variant_img:{variant_img}=====variant_price:{variant_price}'
            )
            variant_info.append(
                {
                    'ASIN': variant_ASIN,
                    'name': variant_name,
                    'img': variant_img,
                    'price': variant_price,
                }
            )
    except Exception:
        print('No variant element found')
    else:
        variant_count = len(variant_divs)
        print(f'variant_info : {variant_info}')
        print(f'variant_count : {variant_count}')

    coupon = None
    saving = None
    promotion = None
    # 3.1 找到父元素//*[@id="promoPriceBlockMessage_feature_div"]
    parent = driver.find_element(
        By.XPATH, '//*[@id="promoPriceBlockMessage_feature_div"]'
    )
    try:
        # 3.2 优惠券 找到子元素1//*[@id="couponTextpctch*"](用contain匹配)
        coupon = parent.find_element(
            By.XPATH, '//*[@id[contains(., "couponTextpctch")]]'
        ).text
        # coupon = coupon.replace('|', '')
        # coupon = coupon.replace('Terms', '')
        # coupon = coupon.strip()
        coupon = re.findall(r'[\d%]+', coupon)
    except Exception:
        print('No coupon element found')
    else:
        print(f'coupon : {coupon}')

    try:
        # 3.3 优惠2a 找到子元素2//*[@id="couponBadgepctch*"](用contain匹配)
        saving_a = parent.find_element(
            By.XPATH, '//*[@id[contains(., "couponBadgepctch")]]'
        ).text
        # 3.4 优惠2b 找到子元素3//*[@id="promoMessagepctch*"](用contain匹配)
        saving_b = parent.find_element(
            By.XPATH, '//*[@id[contains(., "promoMessagepctch")]]'
        ).text
        saving = f"{saving_a} {saving_b}"
        saving = saving.replace('|', '')
        saving = saving.replace('Terms', '')
        saving = saving.strip()
    except Exception:
        print('No saving element found')
    else:
        print(f'saving : {saving}')

    try:
        # 父元素//*[@id="applicablePromotionList_feature_div"] 与优惠1 2 不同
        # 3.3 优惠券3 找到元素//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[1]
        parent = driver.find_element(
            By.XPATH, '//*[@id="applicablePromotionList_feature_div"]'
        )
        promotion_a = parent.find_element(
            By.XPATH,
            '//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[1]',
        ).text
        promotion_b = parent.find_element(
            By.XPATH,
            '//*[@id="applicable_promotion_list_sec"]/span/span/a/span[2]/span[2]',
        ).text
        promotion = f"{promotion_a} {promotion_b}"
        promotion = promotion.replace('|', '')
        promotion = promotion.replace('Terms', '')
        promotion = promotion.strip()
    except Exception:
        print('No promotion element found')
    else:
        print(f'promotion : {promotion}')

        # 4.1 获取Amazon's Choice
    amz_choice = None
    try:
        amz_choice = driver.find_element(
            By.XPATH, '//*[@id="acBadge_feature_div"]/div/span[2]/span/span/a'
        ).text
    except Exception:
        print('No Amazon Choice element found')
    else:
        print(f'Amazon Choice : {amz_choice}')

        # 4.2 五点描述 找到父元素//*[@id="feature-bullets"],获取父元素下//*[@id="feature-bullets"]/ul/li 的li中的文本,保存为数组
    bullet_points = []
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="feature-bullets"]/ul')
    except Exception:
        print('No bullet_points element found')
    else:
        lis = parent.find_elements(By.XPATH, './/li')
        for li in lis:
            bullet_points.append(li.text)
        print(f'bullet_points : {bullet_points}')

    # 5. 获取table //*[@id="productOverview_feature_div"]中的信息,用字典保存
    base_info = {}
    try:
        parent = driver.find_element(
            By.XPATH, '//*[@id="productOverview_feature_div"]/div/table'
        )
        trs = parent.find_elements(By.XPATH, './/tbody/tr')
        for tr in trs:
            key = tr.find_element(By.XPATH, 'td[1]').text
            value = tr.find_element(By.XPATH, 'td[2]').text
            base_info[key] = value
    except Exception:
        print('No Basic Info element found')
    else:
        print(f'Basic Info : {base_info}')

        # 6. 获取table //*[@id="productDetails_techSpec_section_1"]中的信息,用字典保存
    dict_data_Details = {}
    try:
        table1 = driver.find_element(
            By.XPATH, '//*[@id="productDetails_techSpec_section_1"]'
        )
        for tr in table1.find_elements(By.TAG_NAME, 'tr'):
            th = tr.find_element(By.TAG_NAME, 'th')
            td = tr.find_element(By.TAG_NAME, 'td')
            key = th.text
            value = td.text
            dict_data_Details[key] = value
    except Exception:
        print('No dict_data_Details element found')
    else:
        print(f'dict_data_Details : {dict_data_Details}')

        # 7. 获取table //*[@id="productDetails_detailBullets_sections1"] 中的信息,用字典保存
    dict_data_Info = {}
    try:
        table2 = driver.find_element(
            By.XPATH, '//*[@id="productDetails_detailBullets_sections1"]'
        )
        for tr in table2.find_elements(By.TAG_NAME, 'tr'):
            th = tr.find_element(By.TAG_NAME, 'th')
            td = tr.find_element(By.TAG_NAME, 'td')
            key = th.text
            value = td.text
            dict_data_Info[key] = value
    except Exception:
        print('No dict_data_Info element found')
    else:
        print(f'dict_data_Info : {dict_data_Info}')

        # 8. 图片 父元素//*[@id="altImages"]/ul
    # 循环点击左边的小图
    ul = driver.find_element(By.XPATH, '//*[@id="altImages"]/ul')
    image_left1 = None
    image_flag = 0
    for li in ul.find_elements(By.TAG_NAME, 'li'):
        # 如果li的class包含template或aok-hidden或videoThumbnail,继续下一个循环
        if (
            'template' in li.get_attribute('class')  # type: ignore
            or 'aok-hidden' in li.get_attribute('class')  # type: ignore
            or 'videoThumbnail' in li.get_attribute('class')  # type: ignore
            or 'sellersprite' in li.get_attribute('id')  # type: ignore
        ):
            continue
        span = li.find_element(By.XPATH, './span/span')

        if image_flag == 0:
            image_left1 = span
        image_flag += 1

        if isSmallImg:
            # 使用ActionsChains点击input
            if input is not None:
                actions.move_to_element(span)
                actions.click(span)
            actions.perform()
            time.sleep(0.2)
    # 获取所有450尺寸的主图链接
    image_main450 = []
    if isSmallImg:
        ul = driver.find_element(By.XPATH, '//*[@id="main-image-container"]/ul')
        for li in ul.find_elements(By.XPATH, 'li'):
            if 'image' in li.get_attribute('class') and 'item' in li.get_attribute( # type: ignore
                'class'
            ): # type: ignore
                img = li.find_element(By.XPATH, './span/span/div/img')
                img_src = img.get_attribute('src')
                image_main450.append(img_src)
        print(image_main450)

    # 遍历父元素下所有元素
    elements = []

    def get_elements(parent):
        children = parent.find_elements(By.XPATH, './*')
        for child in children:
            elements.append(child)
            get_elements(child)
        return elements

    # 8.1 获取视频数量
    video_count = 0
    try:
        video_text = driver.find_element(By.XPATH, '//*[@id="videoCount"]').text.strip()
        if video_text == "VIDEO":
            video_count = 1
        elif video_text == "VIDEOS":
            video_count = 1
        elif 'VIDEOS' in video_text:
            # \d+ 表示匹配一个或多个数字,这是一个正则表达式,而不是一个字符串。所以这里使用转义序列 \d 是正确的,不会产生无效的转义序列错误。
            # 但是,Pylance 分析器误以为这是一个字符串,所以报告了无效的转义序列错误。
            # 在字符串开头添加 r 会让 Pylance 知道这是一个原始字符串,实际上是正则表达式,可以安全地使用转义序列。
            numbers = re.findall(r'\d+', video_text)
            video_count = int(''.join(numbers))
    except Exception:
        print('No videoCount element found')
    else:
        print(f'videoCount : {video_count}')
        
    if is_Seller:
        try:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]')))
            seller_parent = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
            seller_Linechart = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[2]/div/div[1]/div[1]/div[2]/span')
            actions.move_to_element(seller_Linechart)
            actions.click(seller_Linechart)
            actions.perform()
            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')))
            seller_canvas = seller_parent.find_element(By.XPATH, '//*[@id="quick-view-page"]/div[2]/div/div[2]/div/div/div/div/div/div[1]/canvas')
            seller_selector = seller_parent.find_element(By.CLASS_NAME,'rang-div')
            seller_selector_p = seller_selector.find_elements(By.TAG_NAME,'p')
            if seller_selector_p[-2].find_element(By.XPATH,'./span').text == '最近一年':
                actions.move_to_element(seller_selector_p[-2])
                actions.click(seller_selector_p[-2])
                actions.perform()
            else:
                actions.move_to_element(seller_selector_p[-1])
                actions.click(seller_selector_p[-1])
                actions.perform()
            #folder = r'D:\AutoRPA\卖家精灵\ASIN'
            #asin_folder = folder.replace('ASIN', str(ASIN))
            folder = f'D:\\AutoRPA\\卖家精灵\\{ASIN}'
            if not os.path.exists(folder):
                os.makedirs(folder)
            seller_canvas.screenshot(f'{folder}\\seller_canvas.png')
            seller_quickiew = driver.find_element(By.XPATH,'//*[@id="seller-sprite-extension-quick-view-listing"]')
            # 获取元素的x,y坐标
            x = seller_quickiew.location['x']
            y = seller_quickiew.location['y']
            # 滚动页面,使元素顶部与页面顶部对齐
            driver.execute_script(f"window.scrollTo(0, {y});")
            # 截取指定区域
            driver.get_screenshot_as_file('screenshot.png')
            img = Image.open('screenshot.png')
            # 将元素顶部与页面顶部对齐后，y=0
            img = img.crop((x, 0, x+550, 290)) 
            img.save(f'{folder}\\seller_quickview.png')
        except Exception as e:
            print('No Seller element found')
        
        try:
            seller_parent = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]')
            # 回滚至顶部
            driver.execute_script("window.scrollTo(0, 0);")
            seller_logo = driver.find_element(By.XPATH,'//*[@id="quick-view-page"]/div[1]/div[1]/a/img')
            # 悬停至元素上
            actions.move_to_element(seller_logo)
            actions.perform()
            location = seller_parent.location
            size = seller_parent.size
            print(location)
            print(size)
            actions = ActionChains(driver)
            # 相对与当前位置偏移
            actions.move_by_offset(1412, 180)
            actions.click()
            actions.perform()
            time.sleep(2)
            # 如何处理下载失败？
        except Exception as e:
            print('No Rank Download Fialure element found')

    image_main1500 = []
    # 9. 如果参数isBigImg为真，获取1000+的大尺寸主图
    if isBigImg:
        try:
            # 先点击第一张主图(侧边栏)
            # image_left1 = driver.find_element(By.XPATH, '//*[@id="a-autoid-6"]')
            actions.move_to_element(image_left1)
            actions.click(image_left1)
            actions.perform()
            # 找到图片弹窗元素,模拟点击 //*[@id="imgTagWrapperId"]无法被点击？
            # 部分ASIN 没有[@id="landingImage"] 有class=landingImage
            main_image_element = driver.find_element(
                By.XPATH, '//*[@id="main-image-container"]'
            )
            image_popup = main_image_element.find_element(
                By.XPATH, './/div[@class="imgTagWrapper"]/img'
            )
            # image_popup = driver.find_element(By.XPATH, '//*[@id="landingImage"]')
            actions.move_to_element(image_popup)
            actions.click(image_popup)
            actions.perform()

            # 等待a-popover-content元素出现 //*[@id="ivImagesTabHeading"]/a
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ivImagesTabHeading"]/a')
                )
            )

            # 找到父元素,和子元素div class="ivRow"
            parent = driver.find_element(By.XPATH, '//*[@id="ivThumbs"]')
            divs = parent.find_elements(By.XPATH, './/div[@class="ivRow"]')
            elements = []
            for div in divs:
                des_div = div.find_elements(By.XPATH, './div')
                for ddiv in des_div:
                    elements.append(ddiv)

            # 依次点击elements中的元素,并获取图片链接
            for element in elements:
                actions.move_to_element(element)
                actions.click(element)
                actions.perform()
                time.sleep(0.5)
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="ivLargeImage"]/img')
                    )
                )
                img = driver.find_element(By.XPATH, '//*[@id="ivLargeImage"]/img')
                img_url = img.get_attribute('src')
                while 'loading' in img_url:  # type: ignore
                    time.sleep(0.5)
                    img_url = img.get_attribute('src')
                image_main1500.append(img_url)

            time.sleep(2)
            
            # 添加点击左上角向下偏移200位置
            
            '''image_close = driver.find_element(
                By.XPATH,
                '//button[contains(@class, "a-button-close") and @data-action="a-popover-close" and not(contains(@class, "vse-close-button"))]',
            )
            actions.move_to_element(image_close)
            actions.click(image_close)
            actions.perform()'''
            
            time.sleep(1)
        except Exception:
            print('No description element found')
        else:
            print(f'image_main1500 : ,{image_main1500}')

    time.sleep(2)
    
    # 网页截图
    if is_Keepa:
        print('Keeepa截图')

    if is_Seller:
        print('Seller截图')

    # 10. 获取详情页的文本和图片链接
    # 20230720:先进行读取所有文本，再进行除重，最后合成文本
    description = []
    image_description = []
    img_src = ''
    description_srt = ''
    try:
        parent = driver.find_element(By.XPATH, '//*[@id="aplus_feature_div"]')
        elements = get_elements(parent)
        for element in elements:
            if (
                element.tag_name == 'p'
                or element.tag_name.startswith('h')
                or element.tag_name.startswith('h1')
                or element.tag_name.startswith('h2')
                or element.tag_name.startswith('h3')
                or element.tag_name.startswith('h4')
                or element.tag_name.startswith('h5')
                or element.tag_name == 'span'
            ):
                description.append(element.text)
            elif element.tag_name == 'img':
                img_src = element.get_attribute('data-src')
            if img_src:
                image_description.append(img_src)

    except Exception:
        print('No description element found')
    else:
        # 去除重复的元素
        image_description = remove_duplicates(image_description)

        description_srt = ''
        for item in description:
            if item == '':
                continue
            description_srt += item + '\n'
        description_srt = description_srt.strip()
        print(f'description_srt : {description_srt}')
        print(f'image_description : ,{image_description}')
        

    # 关闭当前标签页
    driver.close()

    # 打包成字典
    AMZInfoDict = {}
    AMZInfoDict['链接'] = valurl
    AMZInfoDict['ASIN'] = ASIN
    AMZInfoDict['国家'] = Country
    AMZInfoDict['标题'] = title
    AMZInfoDict['变体'] = variant_info
    AMZInfoDict['isDeal'] = is_Deal
    AMZInfoDict['现价'] = sale_price
    AMZInfoDict['RRP'] = rrp_price
    AMZInfoDict['会员价'] = prime_price
    AMZInfoDict['折扣'] = discount
    AMZInfoDict['评分'] = rating
    AMZInfoDict['评价数'] = review
    AMZInfoDict['品牌'] = brand
    AMZInfoDict['coupon'] = coupon
    AMZInfoDict['saving'] = saving
    AMZInfoDict['promotion'] = promotion
    AMZInfoDict['AmazonChoice'] = amz_choice
    AMZInfoDict['五点描述'] = bullet_points
    AMZInfoDict['展示信息'] = base_info
    AMZInfoDict['产品信息'] = dict_data_Details
    AMZInfoDict['商品信息'] = dict_data_Info
    AMZInfoDict['主图450'] = image_main450
    AMZInfoDict['视频数量'] = video_count
    AMZInfoDict['主图1500'] = image_main1500
    AMZInfoDict['视频数量'] = video_count
    AMZInfoDict['详情描述'] = description_srt
    AMZInfoDict['详情图片'] = image_description
    return AMZInfoDict


def remove_duplicates(nums):
    # 使用集合的特性,将数组转换为集合,重复元素会被自动去除
    nums_set = set(nums)
    # 将集合转换回列表
    return list(nums_set)


# 测试代码
if __name__ == '__main__':
    # valurl1 = 'https://www.amazon.co.uk/dp/B0BHZDZHZM'
    # print(AMZInfo(valurl1, True, True, False, False))
    #valurl2 = 'https://www.amazon.com/dp/B07B6NP36Q'
    #print(AMZInfo(valurl2,True,True,False,True))
    # valurl3 = 'https://www.amazon.com/dp/B09LY1LNGJ'
    # print(AmazonInfo.AMZInfo(valurl3,False,False,False))
    #valurl1 = 'https://www.amazon.co.uk/HINAA-Pcs-Kids-Dinosaur-Toys/dp/B0BFXDTF7D'
    #print(AMZInfo(valurl1, True, True, False, False))
    print('xx')