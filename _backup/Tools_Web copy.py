import os
import time
import requests
from threading import Thread
from requests.adapters import HTTPAdapter

import pandas as pd


def picdownload1(ASIN: str, pic_array: list, dir: str, filename: str , country):
    # 判断目录是否存在,不存在则创建
    if not os.path.exists(dir):
        os.makedirs(dir)

    # 下载图片的线程
    RETRY_TIMES = 5
    RETRY_INTERVAL = 1
    def download(pic_url, file_path):
        
        '''
        1. timeout - 超时时间,可以设置CONNECT和READ超时
        2. retry - 重试对象,可以设置重试策略,比如重试次数、重试间隔等
        3. stream - 是否使用流方式传输数据,设置为True可以避免读取大文件到内存
        4. verify - 是否验证SSL证书
        5. proxies - 使用代理
        所以更正后的重试代码应该是:
        
        python
        from requests.adapters import HTTPAdapter
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=0.5)
        s.mount('https://', HTTPAdapter(max_retries=retries))
        response = s.get(url, timeout=5)
        '''
        
        for i in range(RETRY_TIMES):
            try:
                response = requests.get(pic_url, timeout=5)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                break
            except Exception:
                print(f"Download failed, retrying {i+1}/{RETRY_TIMES}")
                print(f"Download failed after {RETRY_TIMES} retries: {ASIN} {pic_url}")
                time.sleep(RETRY_INTERVAL)                
        '''
        response = requests.get(pic_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        '''
        
    # 启动多线程下载
    threads = []
    for i, pic_url in enumerate(pic_array):
        if 'https://m.media-amazon.com/images' not in pic_url:
            continue
        file_path = f'{dir}/{ASIN}_{country}_{filename}_{i}.jpg'
        threads.append(Thread(target=download, args=(pic_url, file_path)))

    for thread in threads:
        thread.start()

# 从Excel文件中读取数据
download_info = pd.read_excel('D:/Code/# LISTING/产品图片/ASIN_图片链接_450.xlsx')

def picdownload(ASIN: str, pic_array: list, dir: str, filename: str , country, link):
    global download_info  # 声明为全局变量，可以在函数中修改他的值

    # 判断目录是否存在,不存在则创建
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # 开始下载
    threads = []
    #!for i, pic_url in enumerate(pic_array):
        # 如果链接存在就更新数据，不存在就插入新的数据
        if pic_url in download_info['链接'].values:
            download_info.loc[download_info['链接'] == pic_url, ['ASIN', '国家', f'image_450_{i+1}']] = [ASIN, country, pic_url]
        else:
            new_data = pd.Series([pic_url, ASIN, country, pic_url] + [None]*12, index=download_info.columns)
            #ew_data = {'链接':pic_url, 'ASIN':ASIN, '国家':country, f'image_450_{i+1}':pic_url}
            download_info = download_info.append(new_data, ignore_index=True)
        
        # 启动下载线程
        file_path = f'{dir}/{ASIN}_{country}_{filename}_{i+1}.jpg'
        thread = Thread(target=download, args=(pic_url, file_path, ASIN, i+1))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

# 下载文件并更新下载信息
def download(pic_url, file_path, ASIN, pic_index):
    global download_info
    RETRY_TIMES = 5
    RETRY_INTERVAL = 1
    for i in range(RETRY_TIMES):
        try:
            response = requests.get(pic_url, timeout=5)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            download_info.loc[download_info['链接'] == pic_url, f'image_450_{pic_index}_download'] = "TRUE"  # 更新下载状态
            download_info.to_excel('D:/Code/# LISTING/产品图片/ASIN_图片链接_450.xlsx', index=False)  # 保存更改
            break
        except Exception:
            print(f"Download failed, retrying {i+1}/{RETRY_TIMES}")
            if i == RETRY_TIMES - 1:
                print(f"Download failed after {RETRY_TIMES} retries: {ASIN} {pic_url}")
                time.sleep(RETRY_INTERVAL)

def picdownload2(ASIN: str, pic_array: list, dir: str, filename: str , country, url):
    # 判断目录是否存在,不存在则创建
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # 下载图片的线程
    RETRY_TIMES = 5
    RETRY_INTERVAL = 1
    def download(pic_url, file_path, pic_index):
        global download_info
        for i in range(RETRY_TIMES):
            try:
                response = requests.get(pic_url, timeout=5)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                # 下载成功后更新dataframe
                download_info.loc[ASIN, f'image_450_{pic_index}_download'] = "TRUE"
                break
            except Exception:
                print(f"Download failed, retrying {i+1}/{RETRY_TIMES}")
        else:
            print(f"Download failed after {RETRY_TIMES} retries: {ASIN} {pic_url}")
            time.sleep(RETRY_INTERVAL)  
    
    # 更新记录和启动多线程下载
    threads = []
    for i, pic_url in enumerate(pic_array):
        if 'https://m.media-amazon.com/images' not in pic_url:
            continue
        file_path = f'{dir}/{ASIN}_{country}_{filename}_{i+1}.jpg'
        # 更新dataframe
        download_info.loc[ASIN, '链接'] = url
        download_info.loc[ASIN, 'ASIN'] = ASIN
        download_info.loc[ASIN, '国家'] = country
        download_info.loc[ASIN, f'image_450_{i+1}'] = pic_url
        threads.append(Thread(target=download, args=(pic_url, file_path, i+1)))

    for thread in threads:
        thread.start()

def piccompare():
    return True

img_list = ['https://m.media-amazon.com/images/S/aplus-media-library-service-media/bc65a8d0-e7e6-4ae0-b537-a8a35bb65ead.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/0582c7d9-3b4e-47f0-aaf4-10efa7d6f629.__CR0,0,300,400_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/ff0c023e-f208-41b6-b4fb-d507f37408d3.__CR0,0,300,300_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/5220da0f-ba34-4ebb-bb5a-3347844eb832.__CR0,0,350,175_PT0_SX350_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/3f2897b5-d435-4a94-a1ee-5d9abafeaf54.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/d08b3044-d5a0-447c-a614-a6ecab4f9f10.__CR0,0,970,300_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/f29d9999-1903-4d66-a083-2b11fa542701.__CR0,0,300,300_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/7701fa4e-e967-425f-8780-24a789ee0406.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/d6b01f61-da01-49b7-918a-e7f80ab4fde4.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/b1e1ad4c-5708-422b-ad8f-8cedf3a0bb74.__CR0,0,300,300_PT0_SX300_V1___.jpg']
url = 'https://www.amazon.com/dp/B0C6993ST3'
asin = 'B0C6993ST3'
picture_file_path = r'D:\AutoRPA\产品图片\'
image_dir = f'{picture_file_path}/{asin}/'
