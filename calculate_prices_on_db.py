import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from modules.sqlite_db import SQLiteDatabase

from modules.background_pricecheck import car, car_background_information

#set up db
Car_database = SQLiteDatabase(db_path="used_cars.db")
Car_database.update_table()
#set up autotrader price scraping
autotrader_price_db = car_background_information(driver="chrome",postal_code="TR17%200BJ")

#get the car database that we will calculate the prices on 
car_filters = {
    "ValuationRange" : lambda x: x is None,
     "CarStatus": lambda x: x != "Sold", # otherwise it will try to scrape  urls which are down
    "Manufacturer": lambda x: x == 'Mercedes'
    # "Reg": lambda x : x == "CF17FSL"
   # "ValuationPercentage": lambda x: x is None,
   
    # "Price": lambda x: x < 10000
}
db = Car_database.return_as_panda_dataframe()
sort_database = Car_database.filter_table(db=db, filters=car_filters)
internal_db = sort_database
print(internal_db, flush=True)
Car_database.close_db() # close db now incase another app needs to import

cars_to_get_extra_information = []
print(f"Number of cars {internal_db.count()['id']}", flush=True)
for index, row in internal_db.iterrows(): #print and then create a master car object
    car_reg = row["Reg"]
    car_model = row["Model"]
    car_make = row["Manufacturer"]
    car_mileage = row["Mileage"]
    car_year = row["Year"]
    print(f"VERBOSE: Going to work on {car_reg}: {car_model}", flush=True)
    this_car = car(car_make=car_make, car_model=car_model, mileage=car_mileage, reg=car_reg, year=car_year)
    cars_to_get_extra_information.append(this_car)
print(f"imported {len(cars_to_get_extra_information)}", flush=True)
    

        #import car to scraping database
for import_car_to_scrape in cars_to_get_extra_information:
        autotrader_price_db.add_car(import_car_to_scrape)
        


print("Will start scraping prices now ", flush=True)
autotrader_price_db.series_scrape_autotrader_price(worker_threads=2, timeout_time=25)




Car_database.open_db()  # open db now to import
for  car_data in autotrader_price_db.get_all_cars():

    price_column_index = internal_db.columns.get_loc("Price")
    reg = car_data[0]
    current_price = Car_database.retrieve_db(column="Reg",input_data=reg)[0][price_column_index]
    print(f"Working on {reg} with {current_price}", flush=True)

    car_valuation = autotrader_price_db.get_car_range_price(reg=reg)

    values = autotrader_price_db.get_autotrader_prices(reg=reg)
    precentage_bound = autotrader_price_db.get_car_percentage_range(reg=reg, price_to_check=current_price)

    print(f"For car {reg} £{current_price}. Estimate is {car_valuation}. Percent range is {precentage_bound}%", flush=True)
    #import to db
    Car_database.import_car_properties(
        Reg=reg,
        ValuationPercentage= precentage_bound,
        ValuationRange= car_valuation
    )
print(f"Printing imported table", flush=True)
internal_db = Car_database.return_as_panda_dataframe()
Car_database.close_db()
print(internal_db, flush=True)
