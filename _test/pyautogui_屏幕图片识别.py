import time
import cv2
from PIL import ImageGrab
from ctypes import windll  
import numpy as np
import pyautogui

'''
# 等待一段时间，确保页面加载完成
time.sleep(5)

try:
    # 读取要识别的图片（假设文件名为target_image.png）
    target_image = 'D:\\Code\\Amazon_Selenium\\Resource\\下载.png'

    # 在屏幕上查找目标图片，并获取其位置
    location = pyautogui.locateOnScreen(target_image)

    if location is not None:
        # 获取图片中心点的坐标
        x, y = pyautogui.center(location)

        # 点击图片中心点坐标
        pyautogui.click(x, y)
        print("点击操作成功")
    else:
        print("未找到目标图片")
except Exception as e:
    print("操作失败：", e)
'''
# 模板图片
template = cv2.imread('D:\\Code\\Amazon_Selenium\\Resource\\download2.jpg', 0)  

# 遍历所有屏幕
for i in range(windll.user32.GetSystemMetrics(0)):
    left = windll.user32.GetSystemMetrics(76) * i
    right = left + windll.user32.GetSystemMetrics(76)
    top = windll.user32.GetSystemMetrics(77)
    bottom = windll.user32.GetSystemMetrics(78)
    
    # 获取屏幕区域图像
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 模板匹配
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    threshold = 0.8
    if max_val >= threshold:
        # 转换为绝对屏幕坐标
        x = max_loc[0] + left
        y = max_loc[1] + top
        
        # 使用PyAutoGUI移动实际鼠标
        pyautogui.moveTo(x, y)