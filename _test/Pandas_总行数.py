import pandas as pd


sheet_array = pd.read_excel('D:\\AutoRPA\\产品信息\\'+'ASIN_Array_抓取队列.xlsx', sheet_name='Sheet1')
sheet_info = pd.read_excel('D:\\AutoRPA\\产品信息\\'+'ASIN_Array_信息汇总.xlsx',sheet_name='Sheet1')

# 1. 使用 .shape 属性:
total_rows = sheet_array.shape[0]  # shape[0] 表示行数
print(f'# 1. total_rows : ,{total_rows}')
total_cols = sheet_array.shape[1]  # shape[0] 表示行数
print(f'# 1. total_cols : ,{total_cols}')

# 2. 使用 .iloc 索引器访问最后一行的索引,再加 1:
last_row = sheet_array.iloc[-1, :]  
total_rows = last_row.name + 1  # type: ignore # Name: 8, dtype: object
print(f'# 2. last_row : ,{last_row}')
print(f'# 2. total_rows : ,{total_rows}')

# 3. 使用 pd.read_excel 属性的 RangeIndex RangeIndex(start=0, stop=9, step=1)
RangeIndex = sheet_array.index # type: ignore
row_start = RangeIndex.start   # type: ignore
row_stop = RangeIndex.stop # type: ignore
print(f'# 3 RangeIndex : ,{RangeIndex}')
print(f'# 3 row_start : ,{row_start}')
print(f'# 3 row_stop : ,{row_stop}')

# 3. 使用 .index 属性的 size 属性:
# 设置索引后,sheet_array 的索引类型变为默认的 RangeIndex,它不支持 .count() 方法
#sheet_array_A = sheet_array.set_index('链接')
#rows_info = sheet_array_A.index # type: ignore
#index_count = rows_info.count # type: ignore  'NoneType' object has no attribute 'index'
#print(f'# 3 rows_info : ,{rows_info}')
#print(f'# 3 index_count : ,{index_count}')

# 4. 使用 .count() 统计 DataFrame 索引的数量: 
#total_rows = sheet_array. # type: ignore
#print(f'# 4 total_rows : ,{total_rows}==》》')