import cv2
from PIL import ImageGrab
from ctypes import windll  
import numpy as np
import pyautogui

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