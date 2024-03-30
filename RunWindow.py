import tkinter as tk                                                   # 用于创建窗口
import tkinter.ttk as ttk                                              # 用于创建控件
import tkinter.messagebox as messagebox                                # 用于创建对话框
import ttkthemes                                                       # 用于设置主题
from ttkbootstrap import Style

def ButtonClick():                                                     # 创建一个函数，用途：
    messagebox.showinfo(title="Hello World!", message="Hello World!")  # 显示一个对话框

window = tk.Tk()                                                       # 创建窗口实例
window.geometry("800x600")                                             # 设置窗口大小（可略），有控件这个可以不用
win = ttk.Frame(window)                                                

# ttkbootstrap主题
style = Style(theme='lumen')
'''
light
cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
dark
cyborg - darkly - solar - superhero
'''
# ttkthemes主题
# 因为 ttkthemes 设置的主题对 tkinter 创建的窗口没有效果，并且部分主题要设置背景,所以创建一个 ttk.Frame 承载控件
#style = ttkthemes.ThemedStyle(window)                                  # 设置需要设置主题的窗口
#style.set_theme("black")                                              # 向对应窗口设置主题
'''
['adapta', 'aquativo', 'arc', 'black', 'blue', 'breeze', 'clearlooks', 'elegance', 
'equilux', 'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 
'scidgrey', 'scidmint', 'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'winxpblue', 'yaru']
'''
label = ttk.Label(win, text="Hello World!")                            # 创建一个 Label 标签
progress = ttk.Progressbar(win)                                        # 创建一个 progress 进度条
button = ttk.Button(win, text="Hello World!", command=ButtonClick)     # 创建一个 button 按钮
progress['value'] = 50                                                 # 设置进度条的值
label.pack()                                                           # 显示 label 标签
progress.pack()                                                        # 显示进度条
button.pack()                                                          # 显示按钮
win.pack()                                                             # 显示用于承载控件的 ttk.Frame
window.mainloop()                                                      # 常驻窗口
