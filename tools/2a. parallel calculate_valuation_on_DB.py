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

#set up db
Car_database = SQLiteDatabase(db_path="used_cars.db")

#set up autotrader price scraping
autotrader_price_db = car_background_information(driver="chrome",postal_code="TR17%200BJ")

#print the car database that we will calculate the prices on 
internal_db = Car_database.return_as_panda_dataframe()


cars_to_get_extra_information = []
for index, row in internal_db.iterrows(): #print and then create a master car object
    car_reg = row["Reg"]
    car_model = row["Model"]
    car_make = row["Manufacturer"]
    car_mileage = row["Mileage"]
    car_year = row["Year"]
    print(f"VERBOSE: Going to work on {car_reg}: {car_model}", flush=True)
    this_car = car(car_make=car_make, car_model=car_model, mileage=car_mileage, reg=car_reg, year=car_year)
    cars_to_get_extra_information.append(this_car)

#import car to scraping database
for import_car_to_scrape in cars_to_get_extra_information:
    autotrader_price_db.add_car(import_car_to_scrape)


print("Will start scraping prices now")
autotrader_price_db.parallel_scrape_autotrader_price(worker_threads=4)


for car_data in autotrader_price_db.get_all_cars():
    reg = (car_data[1].reg)
    price = Car_database.retrieve_db(column="Reg",input_data=reg) 

    car_valuation = autotrader_price_db.get_car_range_price(reg=reg)
    current_price = (price[0][4])
    values = autotrader_price_db.get_autotrader_prices(reg=reg)
    precentage_bound = autotrader_price_db.get_car_percentage_range(reg=reg, price_to_check=current_price)

    print(f"For car {reg} £{current_price}. Estimate is {car_valuation}. Percent range is {precentage_bound}%")

