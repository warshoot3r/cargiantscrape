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
#get autotrader variables for naming



cargiant = WebScraperCargiant(driver="chrome", keepalive=False)

url = "https://www.cargiant.co.uk/car/Suzuki/Celerio/LM67FFV"
car_data = cargiant.get_car_details(url, debug=True)






