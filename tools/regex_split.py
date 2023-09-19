import re 
DoorsAndType = "3 Dr Hatch"

DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)
print(DoorsAndType_split, flush=True)

for item in DoorsAndType_split:
          print(item, flush=True)
          if (re.match(r'\d', item)):
               number_doors, bodyType= item.split(" ", 1)
               print(number_doors, flush=True)
               print(bodyType, flush=True)

