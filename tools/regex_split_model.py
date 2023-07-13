import re 
model = "BMW 2 Series Tourer"

model_split = re.split(r'(^\s*[\w]+)\b', model)
model_split = [item for item in model_split if item]
print(model_split [0])

print(model_split [1])