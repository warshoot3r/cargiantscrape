import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
from modules.background_pricecheck import car, car_background_information
import credentials
import re
import time


# Init
force_scrape = True

api_token = credentials.api_token
chat_id = credentials.chat_id

bot = TelegramBot(api_token)
DB = SQLiteDatabase()
car_extra_information = car_background_information(driver="chrome",postal_code="TR17%200BJ")
car_giant = WebScraperCargiant(driver="chrome",keepalive=False)

scraped_data = car_giant.search_for_manufacturer_with_bmw_or_mercedes(manufacturer="BMW",numberofpages=0)

#import car to DB

for i in range(car_giant.length):
    current_car = car_giant.data.iloc[i]
    DB.import_car_properties(
            Body_Type=current_car["Body Type"],
            Color=current_car["Color"],
            Doors=current_car["Doors"],
            Manufacturer=current_car["Manufacturer"],
            Year=current_car["Year"],
            Price=current_car["Price"],
            Transmission=current_car["Transmission"],
            Fuel=current_car["Fuel"],
            Reg=current_car["Reg"],
            URL=current_car["URL"],
            Model=current_car["Model"],
            Mileage=current_car["Mileage"],
            CarStatus=current_car["Car Status"]
    )


data = DB.return_as_panda_dataframe()

DB.print_as_panda_dataframe(table=data)