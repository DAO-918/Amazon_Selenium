import requests
from lxml import etree
import pandas as pd
import re

# 创建表格
columns = ['链接', '标题', '时间', '标签', '特征码']
data = []

# 定义页码范围
start_page = 1 
end_page = 10 

for page in range(start_page, end_page + 1):
    # 步骤1: 从request获取网页数据
    response = requests.get(f'https://www.bbb.zip/wp/category/all/comic/page/{page}')  
    html = response.text

    # 步骤2: 获取父元素下所有标签为article的子元素
#    root = etree.HTML(html)
    
