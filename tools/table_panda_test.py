import pandas as pd

# Create a table data
data = {
     'Model': ["Test"],
     "Year": [0],
     "Details": ["Test"]
}


#Create dataframe object
df = pd.DataFrame(data)


#Add a row
new_data =  {
    "Model": "Fiesta",
    "Year": 2010,
    "Details": "pretty good car"
}
df.loc[1] = new_data



#print data
print(df)