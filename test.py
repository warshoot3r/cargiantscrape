from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
DB = SQLiteDatabase()


data = DB.return_as_panda_dataframe()
cars = WebScraperCargiant(driver="chrome", keepalive=True)


filter = {

    'Price': lambda x: x >= 17000,
    'Year': lambda x: x == 2018,
    'Manufacturer': lambda x: x == "BMW"
    }
print(data[["Price", "Model", "Reg"]])
array = ["SJ68BWP", "YK16ETD", "YH16JUK"]
data_filter = DB.filter_table( filter, data)
print(data_filter)


