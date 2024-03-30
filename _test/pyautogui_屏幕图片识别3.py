import pyautogui
import cv2
from PIL import ImageGrab
from ctypes import windll  
import numpy as np
import pyautogui

# 模板图片的路径
template_path = r"D:\Code\Amazon_Selenium\Resource\download2.jpg"

def find_template_on_screen(template_path):
    # 进行模板匹配，找到模板在屏幕上的位置
    try:
        position = pyautogui.locateOnScreen(template_path)
        if position is None:
            raise Exception("未找到模板图片")
        return position
    except Exception as e:
        print("模板匹配出错:", str(e))
        return None

def move_mouse_to_position(position):
    # 计算目标位置的中心坐标
    target_x = position.left + position.width / 2
    target_y = position.top + position.height / 2
    
    # 获取当前鼠标位置，以便于计算相对移动距离
    current_x, current_y = pyautogui.position()
    
    # 计算鼠标需要移动的距离
    move_x = target_x - current_x
    move_y = target_y - current_y
    
    # 实际移动鼠标
    pyautogui.move(move_x, move_y, duration=0.5)

def main():
    # 查找模板在屏幕上的位置
    template_position = find_template_on_screen(template_path)
    if template_position:
        print("找到模板图片，位置：", template_position)
        move_mouse_to_position(template_position)
    else:
        print("未找到模板图片")

if __name__ == "__main__":
    main()
