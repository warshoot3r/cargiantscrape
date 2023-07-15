import pandas as pd

# Example data for two tables
data1 = {'Name': ['John', 'Alice'],
         'Age': [30, 25]}
table1 = pd.DataFrame(data1)

data2 = {'Name': ['Bob', 'Eve'],
         'Age': [35, 27]}
table2 = pd.DataFrame(data2)

# Stack the rows vertically
stacked_table = pd.concat([table1, table2], axis=0)

# Print the stacked table
print(stacked_table)