# python code to test logic names for adjusting the algorhtynm
import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from selenium import webdriver
import time
import bs4
from selenium.webdriver.common.by import By
import re
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.sqlite_db import SQLiteDatabase 
#get autotrader variables for naming


cargiant = WebScraperCargiant(driver="chrome", keepalive=False)

db = SQLiteDatabase(db_path='used_cars.db')


filters = {

    "Manufacturer": lambda x: x == "BMW"
}
db_data = db.return_as_panda_dataframe()
data = db.filter_table(db=db_data, filters=filters)

print(data)



list_of_url_regs = data["URL"]

for url in list_of_url_regs:
    # url = "https://www.cargiant.co.uk/car/Suzuki/Celerio/LM67FFV"
    car_data = cargiant.get_car_details(url, debug=True)






