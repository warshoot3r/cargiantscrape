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


# Init
force_scrape = True

api_token = credentials.api_token
chat_id = credentials.chat_id

bot = TelegramBot(api_token)
DB = SQLiteDatabase()
cg = WebScraperCargiant(driver="chrome", keepalive=False)




very_ideal_filters = {
   'Price': lambda x: x >= 9000,   
    'Price': lambda x: x <=16000,
    'Mileage': lambda x: x <=60000,
    'Year': lambda x: x >= 2017,
    "Engine Size": lambda x: x >= "2.0",
    "CarStatus": lambda x: x != "Sold",
    # "Transmission": lambda x: x == "Auto",
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
    # 'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"), 
    # 'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}

data = DB.return_as_panda_dataframe()
print(DB.filter_table(db=data, filters=very_ideal_filters)["ValuationPercentage"])