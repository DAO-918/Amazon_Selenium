col = 68

if col < 26:
  column = chr(col + 64) 
else:
  column = chr(col // 26 + 64) + chr(col % 26 + 64)
  
print(column)