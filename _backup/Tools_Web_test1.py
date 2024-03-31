import pandas as pd
import os
import requests 
from threading import Thread
import time



def picdownload(url, ASIN, country, pic_array: list, dir, filename):
    global download_info 
    download_info = pd.read_excel('D:/Code/# LISTING/产品图片/ASIN_图片链接_450.xlsx', index_col=1)
    # 判断目录是否存在,不存在则创建
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # 下载图片的线程
    RETRY_TIMES = 5
    RETRY_INTERVAL = 1
    
    # 10列图片对应_download的column
    cols_pic = [f'image_450_{i+1}' for i in range(10)]
    cols_download = [f'image_450_{i+1}_download' for i in range(10)]
    
    def download(pic_url, file_path, pic_index):
        for i in range(RETRY_TIMES):
            try:
                response = requests.get(pic_url, timeout=5)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                download_info.loc[url, cols_download[pic_index]] = "TRUE"
                break
            except Exception:
                print(f"Download failed, retrying {i+1}/{RETRY_TIMES}")
        else:
            print(f"All attempts to download have failed: {ASIN} {pic_url}")
            time.sleep(RETRY_INTERVAL)  
    # 更新记录和启动多线程下载
    threads = []
    if url not in download_info.index.values:
        for i, pic_url in enumerate(pic_array):
            if 'https://m.media-amazon.com/images' not in pic_url:
                continue
            if download_info.loc[url, cols_pic[i]] != pic_url: # 判断图片链接改变
                download_info.loc[url, cols_pic[i]] = pic_url
                download_info.loc[url, cols_download[i]] = "FALSE"
                file_path = f'{dir}/{ASIN}_{country}_{filename}_{i+1}.jpg'
                threads.append(Thread(target=download, args=(pic_url, file_path, i)))
                
    elif url in download_info.index.values:
        total_rows = len(download_info)
        # 修改对应的列的值
        data_new = pd.Series([""]*len(download_info.columns), index=download_info.columns)
        data_new['链接'] = url
        data_new['ASIN'] = ASIN
        data_new['国家'] = country
        download_info = download_info.append(data_new, ignore_index=True)
        for i, pic_url in enumerate(pic_array):
            if 'https://m.media-amazon.com/images' not in pic_url:
                continue
            download_info.loc[url, cols_pic[i]] = pic_url
            download_info.loc[url, cols_download[i]] = "FALSE"
            file_path = f'{dir}/{ASIN}_{country}_{filename}_{i+1}.jpg'
            threads.append(Thread(target=download, args=(pic_url, file_path, i)))
        
    # 启动所有线程
    for thread in threads:
        thread.start()
    # 等待所有线程执行完成 
    
    for thread in threads:
        thread.join()
    download_info.to_excel(f'D:/Code/# LISTING/产品图片/ASIN_图片链接_450.xlsx', index=False)
    
# 测试代码
if __name__ == '__main__':
    url = 'https://www.amazon.com/dp/B0C6993ST3'
    asin = 'B0C6993ST3'
    country = 'us'
    img_list = ['https://m.media-amazon.com/images/I/81Y26toqdTL.__AC_SY300_SX300_QL70_FMwebp_.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/0582c7d9-3b4e-47f0-aaf4-10efa7d6f629.__CR0,0,300,400_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/ff0c023e-f208-41b6-b4fb-d507f37408d3.__CR0,0,300,300_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/5220da0f-ba34-4ebb-bb5a-3347844eb832.__CR0,0,350,175_PT0_SX350_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/3f2897b5-d435-4a94-a1ee-5d9abafeaf54.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/d08b3044-d5a0-447c-a614-a6ecab4f9f10.__CR0,0,970,300_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/f29d9999-1903-4d66-a083-2b11fa542701.__CR0,0,300,300_PT0_SX300_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/7701fa4e-e967-425f-8780-24a789ee0406.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/d6b01f61-da01-49b7-918a-e7f80ab4fde4.__CR0,0,970,600_PT0_SX970_V1___.jpg', 'https://m.media-amazon.com/images/S/aplus-media-library-service-media/b1e1ad4c-5708-422b-ad8f-8cedf3a0bb74.__CR0,0,300,300_PT0_SX300_V1___.jpg']
    picture_file_path = r'D:\AutoRPA\产品图片'
    image_dir = f'{picture_file_path}/{asin}/'
    #download_info = pd.read_excel('D:/Code/# LISTING/产品图片/ASIN_图片链接_450.xlsx')
    picdownload(url, asin, country, img_list, image_dir, '450')
