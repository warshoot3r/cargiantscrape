import re 
DoorsAndType = "3 Dr Hatch"

DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)
print(DoorsAndType_split)

for item in DoorsAndType_split:
          print(item)
          if (re.match(r'\d', item)):
               number_doors, bodyType= item.split(" ", 1)
               print(number_doors)
               print(bodyType)

