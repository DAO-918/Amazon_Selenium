from datetime import datetime

#print(datetime.date.today().strftime('%Y/%m/%d'))

time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time)

#- datetime.datetime.now() 返回带时间的datetime对象
#- datetime.date.today() 只返回日期的date对象