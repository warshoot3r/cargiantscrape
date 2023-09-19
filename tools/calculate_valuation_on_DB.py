# script.py

import sys
import os

# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
import re
import time
from modules.background_pricecheck import car,car_background_information
from modules.autotrader_naming import autotrader_naming


DB = SQLiteDatabase(db_path="used_cars.db")

print(f"printing database: {SQLiteDatabase.return_as_panda_dataframe()}", flush=True, flush=True)
car_extra_information = car_background_information(driver="chrome",postal_code="TR17%200BJ")


