from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import time
import platform

#Create DB 
DB = SQLiteDatabase()

#create Telegrambot
tb = TelegramBot(api_token=33)
print("Successful teleegram bot init", flush=True)

data = DB.return_as_panda_dataframe()

#Create selenium
cars = WebScraperCargiant(driver="chrome", keepalive=True)
print("Successful selenium init", flush=True)
# test 1
cars.get_car_makes()

print("Successful Car makes init", flush=True)
#test 2
filter = {

    'Price': lambda x: x >= 17000
    }
array = ["MF68CEX", "YK16ETD", "YH16JUK"]
data_filter = DB.filter_table( filter, data, array)
print(data_filter, flush=True)

#test 3 pull data only for amd64 as no emulation isn possible ###



print("Successful filter table", flush=True)
print("===============================", flush=True)
print("Successful execution:", flush=True)
print("Operating System:", platform.system(), flush=True)
print("Architecture:", platform.machine(), flush=True)
if( platform.machine() == "x86_64"):
    print("Testing a 2 page scrape for performance test", flush=True)
    start_time = time.time()
    cars.search_for_manufacturer(manufacturer="BMW", numberofpages=1)
    for i in range(cars.length):
            current_car = cars.data.iloc[i]
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
    end_time = time.time()
    start_time_test_1 = time.time()
    print("Testing raw Database export", flush=True)
    exported_table = DB.print_raw_data_from_sqlite_db()
    database = DB.return_as_panda_dataframe()
    print("Printing a formated DB", flush=True)
    print(DB.print_as_panda_dataframe(database), flush=True)
    end_time_test_1 = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_test_1 = end_time_test_1 - start_time_test_1
    print(f"Execution time for test: web scrape: {elapsed_time:.6f} seconds", flush=True)
    print(f"Execution time for DB functions: web scrape: {elapsed_time_test_1:.6f} seconds", flush=True)

print("===============================")