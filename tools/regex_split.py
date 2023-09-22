import re 
string = "250h"

regex = r"\d{3}\S"

i = re.search(pattern=regex, string=string)
print(i.group(0))
# print(i.group(0))
# print(i.group(2))