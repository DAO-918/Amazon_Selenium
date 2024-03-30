import tkinter as tk                                                   # 用于创建窗口
import tkinter.ttk as ttk                                              # 用于创建控件
import tkinter.messagebox as messagebox                                # 用于创建对话框
import ttkbootstrap as tkstrap
import ttkbootstrap.constants

def ButtonClick():                                                     # 创建一个函数，用途：
    messagebox.showinfo(title="Hello World!", message="Hello World!")  # 显示一个对话框

window = tk.Tk()                                                       # 创建窗口实例
window.geometry("800x600")                                             # 设置窗口大小（可略），有控件这个可以不用
win = ttk.Frame(window)                                                
# ttkbootstrap主题
style = tkstrap.Style(theme='lumen')

b1 = tkstrap.Button(win, text="Button 1", style="success")  # 使用字符串"success"表示成功样式
b1.pack(side=tk.LEFT, padx=5, pady=10)
b2 = tkstrap.Button(win, text="Button 2", style=("info outline"))  # 使用元组表示信息样式和轮廓样式
b2.pack(side=tk.LEFT, padx=5, pady=10)

label = ttk.Label(win, text="Hello World!")                            # 创建一个 Label 标签
progress = ttk.Progressbar(win)                                        # 创建一个 progress 进度条
button = ttk.Button(win, text="Hello World!", command=ButtonClick)     # 创建一个 button 按钮
progress['value'] = 50                                                 # 设置进度条的值
label.pack()                                                           # 显示 label 标签
progress.pack()                                                        # 显示进度条
button.pack()                                                          # 显示按钮
win.pack()                                                             # 显示用于承载控件的 ttk.Frame
window.mainloop()                                                      # 常驻窗口
