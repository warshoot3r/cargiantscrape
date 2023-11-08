import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
from modules.background_pricecheck import car_background_information, car
import credentials

import re
import time

# Init
force_scrape = True

api_token = credentials.api_token
chat_id = credentials.chat_id

bot = TelegramBot(api_token)
DB = SQLiteDatabase()

# # DB.clear_car_valuation_ranges(days=1)
DB.fix_datetime()


data = DB.return_as_panda_dataframe()

# # 
data_cars = DB.get_cars_with_date_updated(3)


# # data = DB.return_as_panda_dataframe()

# # print(data[["Manufacturer","Price", "ValuationRange", "DateUpdated"]])



