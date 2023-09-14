

# get some data from db and scrape the prices from autotrader
import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.sqlite_db import SQLiteDatabase
from modules.background_pricecheck import car_background_information,car

import credentials

db = SQLiteDatabase(db_path="used_cars.db")


filters = {

    'Price': lambda x : x < 20000,
    'Price': lambda x: x >=10000,
    'Model': lambda x : x == "330e"
}
database = db.return_as_panda_dataframe()
db.print_as_panda_dataframe(table=database)
data = db.filter_table(db=database,filters=filters)


db.print_as_panda_dataframe(table=data)

print(data)

car_to_parse = []


for index, row in data.iterrows():

    print(row.Manufacturer, row.Model, row.Mileage, row.Reg, row.Year)
    car_to_parse.append(car(car_make=row.Manufacturer, car_model=row.Model, mileage=row.Mileage, reg=row.Reg, year=row.Year))


car_additional_information = car_background_information(driver="chrome", postal_code=credentials.postal_code)


for pendingcar in car_to_parse:
    car_additional_information.add_car(car=pendingcar)

car_additional_information.scrape_autotrader_price()


for car_data in car_additional_information.get_all_cars():
    reg = (car_data[1].reg)
    price = db.retrieve_db(column="Reg",input_data=reg) 

    car_valuation = car_additional_information.get_car_range_price(reg=reg)
    current_price = (price[0][4])
    values = car_additional_information.get_autotrader_prices(reg=reg)
    precentage_bound = car_additional_information.get_car_percentage_range(reg=reg, price_to_check=current_price)

    print(f"For car {reg} £{current_price}. Estimate is {car_valuation}. Percent range is {precentage_bound}%")
