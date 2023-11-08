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

autotrader = car_background_information(driver="chrome",postal_code="TR17%200BJ")

example_car = car(car_make="BMW",
                  car_model="320D",
                  mileage="55500",
                  year="2018",
                  reg="22"
                  )

autotrader.add_car(example_car)


price = autotrader.series_scrape_autotrader_price()

car_range = autotrader.get_car_range_price(reg="22")

data = DB.return_as_panda_dataframe()


