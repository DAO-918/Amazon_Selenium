import json

list_Str = str([
    'Large Dinosaur Transport Truck – The truck is equipped with a simulated T-rex head which makes it look cooler. And the large cage allows it to capture more dinosaurs. Truck size: 35*15*20cm.',
    '8 Realistic Dinosaur Figures – This play set comes with 2 medium Tyrannosaurus dinosaurs and 6 mini other dinosaurs. All dinosaurs can be captured into the cage. Tips: If you want to catch the bigger dinosaurs, please remove the barrier in the middle of the cage first.',
    'Dinosaur Theme Play Mat – A dinosaur park activity play mat help kids to build their own dinosaur world easily. Mat size is 70*80cm, it is large enough for 2-3 kids to play on the ground.',
    'Durable and Safe – All dinosaurs and truck are made of durable and BPA plastic; mat is made of soft non-woven fabrics instead of thin PVC. The monster truck has four big wheel which make it more stable.',
    'Perfect Gift for Kids – It will be a great gift for kids who love car toys and dinosaurs. Suitable for boys and girls 3 4 5 6 7 years in birthday party, Christmas or other holidays.',
    'TEMI Dinosaur Truck Toys for Kids 3-5 Years, Tyrannosaurus Transport Car Carrier Truck with 8 Dino Figures, Activity Play Mat, Dinosaur Eggs, Capture Jurassic Dinosaur Play Set for Boys and Girls',
])

arr1 = list(list_Str)
print('===============')
print(arr1[2])
print(len(arr1))
'''
L
1248
'''

arr2 = eval(list_Str)
print('===============')
print(arr2[0])
print(len(arr2))
'''
Large Dinosaur Transport Truck – The truck is equipped with a simulated T-rex head which makes it look cooler. And the large cage allows it to capture more dinosaurs. Truck size: 35*15*20cm.
6
'''

# 在使用json.loads()方法前,对字符串进行格式检查与处理,确保其为正确的JSON格式
try: 
    arr3 = json.loads(list_Str)
except Exception as e:
    if list_Str.startswith('[') and list_Str.endswith(']'):
        # 如果是列表字符串,使用eval()加载
        arr = eval(list_Str)
    else:
        # 其他情况,抛出异常或进行其他处理
        raise ValueError('Invalid string format') from e
