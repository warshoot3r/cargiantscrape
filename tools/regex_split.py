import re 
string = "250h F Sport"

regex = r"(\d{3}\S)\s(.*)"

i = re.search(pattern=regex, string=string)

print(i.group(1))
print(i.group(2))