import openpyxl
from openpyxl.drawing.image import Image

path= 'D:\\AutoRPA\\产品信息\\'
wb_path= f'{path}ASIN_Info-.xlsx'
wb = openpyxl.load_workbook(wb_path)
sheet = wb['竞品分析-Part1']

# 设置 I 至 P 列的宽度
for col in range(9, 17):
    sheet.column_dimensions[chr(col + 64)].width = 8

# 在第二行插入图片
flag =  1
img_floder = 'D:\\AutoRPA\\产品图片\\B07TFBGXKC\\'
for col in range(9, 17):
    img_path = f'{img_floder}B07TFBGXKC_450_{flag}.jpg'
    img = Image(img_path)
    # 1字符 = 7px
    img.width = sheet.column_dimensions[chr(col + 64)].width * 8  # type: ignore # 设置图片宽度为列宽
    # 1磅 = 4/3px
    img.height = sheet.row_dimensions[2].height * (4/3)  # type: ignore # 设置图片高度为行高

    sheet.add_image(img, f'{chr(col + 64)}2')

wb.save(wb_path)


