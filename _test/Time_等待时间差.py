import time
import datetime

# 获取当前时间
current_time = datetime.datetime.now()
print(current_time)
current_time = datetime.datetime(2023, 7, 13, 23, 40)
# 当current_time.hour为23时，hour=current_time.hour + 1，hour为24，超出了0-23的范围
if current_time.hour == 23:
    # current_time = current_time.replace(hour=0)
    print(current_time)
    next_hour = current_time.replace(
        day=current_time.day + 1, hour=0, minute=0, second=0, microsecond=0
    )
else:
    next_hour = current_time.replace(
        hour=current_time.hour + 1, minute=0, second=0, microsecond=0
    )
# 计算距离下一个整点的时间差
delta = next_hour - current_time
print(delta)
seconds_to_wait = delta.total_seconds()
minut_to_wait = seconds_to_wait / 60
print(f'{seconds_to_wait}=={minut_to_wait}')
seconds_to_wait = abs(delta.total_seconds())
minut_to_wait = seconds_to_wait / 60
print(f'{seconds_to_wait}=={minut_to_wait}')

# 等待到下一个整点时
# time.sleep(seconds_to_wait)
