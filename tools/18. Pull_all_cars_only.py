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

DB.update_table()
# Filters
filters = {
   'Price': lambda x: x >= 10000,   
    'Price': lambda x: x <=20000,
    'Mileage': lambda x: x <=80000,
    'Year': lambda x: x >= 2015,
    "CarStatus": lambda x: x != "Sold",
    # "Manufacturer": lambda x: x == "lexus",
     # No BMW 1 Series 
    #  'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"), 
    # 'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}

#scrape cars
def scrape_cars():
    if(DB.is_db_recently_written() and not force_scrape):
        print("Not scraping as DB written in last 10 minutes", flush=True)
        time.sleep(2)
        return(False)
    print("Starting", flush=True)
    CarSearch = WebScraperCargiant(driver="chrome", keepalive=True)
    # CarSearch.search_for_manufacturer_with_bmw_or_mercedes(manufacturer="BMW",numberofpages=0)
    # CarSearch.search_for_manufacturer_with_bmw_or_mercedes(manufacturer="Mercedes",numberofpages=0)
    CarSearch.search_for_manufacturer("Lexus")
    CarSearch.print_number_of_cars()
    return CarSearch

#Get new data and import it into DB

def import_cars(CarSearch):
    if(CarSearch):
        for i in range(CarSearch.length):
            current_car = CarSearch.data.iloc[i]
            #print(f"this car with {current_car['Manufacturer']}  {current_car['Reg']} {current_car['Car Status']}", flush=True)
            DB.import_car_properties(
                    Body_Type=current_car["Body Type"],
                    Color=current_car["Color"],
                    Doors=current_car["Doors"],
                    Manufacturer=current_car["Manufacturer"],
                    Year=current_car["Year"],
                    Price=current_car["Price"],
                    Engine_size=current_car["Engine Size"],
                    Transmission=current_car["Transmission"],
                    Fuel=current_car["Fuel"],
                    Reg=current_car["Reg"],
                    URL=current_car["URL"],
                    Model=current_car["Model"],
                    ModelVariant=current_car["Model Variant"],
                    Mileage=current_car["Mileage"],
                    CarStatus=current_car["Car Status"]
            )


# Output a table of data and send it


# Forever loop to poll every 60 minutes

scraped_cars = scrape_cars()
import_cars(scraped_cars)
# print(DB.return_as_panda_dataframe()[[ "Model Variant"]])
print(DB.return_as_panda_dataframe()[["Engine Size","Model", "Model Variant"]])
# price_changed = DB.car_price_changed()
# new_cars = DB.car_new_changed()
# status_changed = DB.car_status_changed()
# if price_changed or new_cars or status_changed:
#     DB.open_db()
#     database = DB.return_as_panda_dataframe()
#     if price_changed: #If car prices changed, only send a list of these cars
#         database_filtered = DB.filter_table(filters, database, DB.get_car_price_changed())
#         database_filtered.loc[:,"PriceChange"] = database_filtered["Price"] - database_filtered["OldPrice"] # should be added to class . temporary here for now
#         bot.send_dataframe(chat_id, database_filtered[["URL", "Manufacturer","Model", "Price", "PriceChange", "Mileage" ]], "New car prices were updated:",  MessageThreadID=credentials.message_id)
#     if new_cars:
#         database_filtered_new_cars = DB.filter_table(filters, database, DB.get_car_new_changed())
#         print(database_filtered_new_cars, flush=True)
#         bot.send_dataframe(chat_id, database_filtered_new_cars[["URL","Manufacturer","Model", "Mileage", "Price"] ], "New cars were added:", True,  MessageThreadID=credentials.message_id) 
#        #Send sold cars
  
#     if status_changed:
#         reg = DB.get_car_status_changed()
#         database_filtered = DB.filter_table(filters, database, reg)
#         print(database_filtered, flush=True)
#         #old way bot.send_dataframe(chat_id, database_filtered[[ "URL","Manufacturer","Model", "CarStatus", "Price"]], "Some car status changed:")

#         # new way send them seperatly
#         table_filters = ["URL","Manufacturer","Model", "Mileage", "Price"]
#         sold = database_filtered.loc[database_filtered['CarStatus'] == "Sold"]
#         if sold.shape[0] > 0:
#             bot.send_dataframe(chat_id, sold[table_filters], caption="Sold Cars",  MessageThreadID=credentials.message_id)

#         reserved = database_filtered.loc[database_filtered['CarStatus'] == "Reserved"]
#         if reserved.shape[0] > 0:
#             bot.send_dataframe(chat_id, reserved[table_filters], caption="Reserved Cars",  MessageThreadID=credentials.message_id)
        
#         available = database_filtered.loc[database_filtered['CarStatus'].str.contains(r'AVAILABLE', case=True, regex=True)]
#         if available.shape[0] > 0:
#             bot.send_dataframe(chat_id, available[[x for x in table_filters] + ["CarStatus"]], "Available soon:", MessageThreadID=credentials.message_id)

#         bot.send_dataframe_as_file(chat_id=chat_id, file_format="csv", dataframe=(DB.get_car_sold_as_pd()), caption="Sold Cars", file_name="sold", MessageThreadID=credentials.message_id)
#           #Send rest of cars
#     csv_dataframe = DB.filter_table(filters, database) # every car

#     # csv_dataframe['CarStatus'].fillna('NA', inplace=True) # fix for NA otherwise we can not use str.contains below

#     not_available_csv = csv_dataframe.loc[csv_dataframe['CarStatus'].str.contains(r'AVAILABLE|Reserved', case=True, regex=True)] # The available cars
#     available_csv = csv_dataframe.loc[csv_dataframe['CarStatus'] == "Available"] # The available cars
#     # bot.send_dataframe_as_file(chat_id=chat_id, file_format="csv", data frame=available_csv, caption="Available Cars", file_name="available")
#     # bot.send_dataframe_as_file(chat_id=chat_id, file_format="csv", dataframe=not_available_csv, caption="Waiting Cars", file_name="waiting")
#     #New way send multiple in one go.
#     data_frames = [available_csv, not_available_csv]
#     file_formats = ["csv","csv"]
#     captions = ["Available Cars", "Waiting Cars"]
#     file_names = ["available", "waiting"]
#     bot.send_dataframe_as_csv_files(captions=captions,chat_id=credentials.chat_id, dataframes=data_frames, file_names=file_names, MessageThreadID=credentials.message_id)


#     DB.close_db()
# else:
#     bot.send_message_servername(chat_id, "Nothing to report", MessageThreadID=credentials.message_id)