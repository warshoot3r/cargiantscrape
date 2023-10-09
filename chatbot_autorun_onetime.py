from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
import re

# Init
force_scrape = True

api_token = credentials.api_token
chat_id = credentials.chat_id

bot = TelegramBot(api_token)
DB = SQLiteDatabase()

CarSearch = WebScraperCargiant(driver="chrome", keepalive=True)


DB.update_table()
# Filters
filters = {
   'Price': lambda x: x >= 10000,   
    'Price': lambda x: x <=30000,
    'Mileage': lambda x: x <=60000,
    'Year': lambda x: x >= 2015,
    "Engine Size": lambda x: x >= "1.5",
    "CarStatus": lambda x: x != "Sold",
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
     'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"), 
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}


very_ideal_filters = {
   'Price': lambda x: x >= 9000,   
    'Price': lambda x: x <=16000,
    'Mileage': lambda x: x <=80000,
    'Year': lambda x: x >= 2017,
    "Engine Size": lambda x: x >= "2.0",
    "CarStatus": lambda x: x != "Sold",
    "Transmission": lambda x: x == "Auto",
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
    'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"), 
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}

#scrape cars
def scrape_cars():
    print("Starting", flush=True)
    CarSearch.search_for_manufacturer_with_bmw_or_mercedes(manufacturer="BMW",numberofpages=0, worker_threads=2)
    CarSearch.search_for_manufacturer_with_bmw_or_mercedes(manufacturer="Mercedes",numberofpages=0, worker_threads=2)
    CarSearch.search_for_manufacturer("Lexus")
    return CarSearch

#Get new data and import it into DB

def import_cars(CarSearch):
    if(CarSearch):
        for i in range(CarSearch.length):
            current_car = CarSearch.data.iloc[i]
            DB.import_car_properties(
                    Body_Type=current_car["Body Type"],
                    Color=current_car["Color"],
                    Doors=current_car["Doors"],
                    Manufacturer=current_car["Manufacturer"],
                    Year=current_car["Year"],
                    Price=current_car["Price"],
                    Transmission=current_car["Transmission"],
                    Fuel=current_car["Fuel"],
                    Engine_size=current_car["Engine Size"],
                    Reg=current_car["Reg"],
                    URL=current_car["URL"],
                    Model=current_car["Model"],
                    ModelVariant=current_car["Model Variant"],
                    Mileage=current_car["Mileage"],
                    CarStatus=current_car["Car Status"]
            )


# Forever loop to poll every 60 minutes

scraped_cars = scrape_cars()
import_cars(scraped_cars)
price_changed = DB.get_car_price_changed(filters)
new_cars = DB.get_car_new_changed(filters)
status_changed = DB.get_car_status_changed(filters)
DB.open_db()
if not(price_changed.empty): #If car prices changed, only send a list of these cars
    database_filtered.loc[:,"PriceChange"] = database_filtered["Price"] - database_filtered["OldPrice"] # should be added to class . temporary here for now
    bot.send_dataframe(chat_id, price_changed[["URL", "Manufacturer","Model", "Price", "PriceChange", "Mileage" ]], "New car prices were updated:",  MessageThreadID=credentials.message_id)
if not(new_cars.empty):
    print(new_cars, flush=True)
    bot.send_dataframe(chat_id, new_cars[["URL","Manufacturer","Model", "Mileage", "Price"] ], "New cars were added:", True,  MessageThreadID=credentials.message_id) 

if not(status_changed.empty):
    print(status_changed, flush=True)
    table_filters = ["URL","Manufacturer","Model", "Mileage", "Price"]
    sold = status_changed.loc[status_changed['CarStatus'] == "Sold"]
    if sold.shape[0] > 0:
        bot.send_dataframe(chat_id, sold[table_filters], caption="Sold Cars",  MessageThreadID=credentials.message_id)

    reserved = status_changed.loc[status_changed['CarStatus'] == "Reserved"]
    if reserved.shape[0] > 0:
        bot.send_dataframe(chat_id, reserved[table_filters], caption="Reserved Cars",  MessageThreadID=credentials.message_id)

    available = status_changed.loc[status_changed['CarStatus'].str.contains(r'AVAILABLE', case=True, regex=True)]
    if available.shape[0] > 0:
        bot.send_dataframe(chat_id, available[[x for x in table_filters] + ["CarStatus"]], "Available soon:", MessageThreadID=credentials.message_id)
    ideal_cars_from_status_changed = DB.filter_table(db=status_changed, filters=very_ideal_filters)
    
    
    # Ideal cars from stricter filter
    if ideal_cars_from_status_changed.shape[0] > 0:
        print(f"Got cars for ideal filter", flush=True)
        bot.send_message(chat_id=credentials.chat_id, message="Got Strict filter cars",MessageThreadID=credentials.message_id)
        urls = ideal_cars_from_status_changed["URL"].to_list()
        picture_data = CarSearch.get_car_url_snapshot(url=urls)
        bot.send_base64pictures(chat_id=credentials.chat_id, base64_data=picture_data, caption="Strict Filter Cars", message_id=credentials.message_id)
        bot.send_dataframe(chat_id=chat_id,dataframe=ideal_cars_from_status_changed, caption="Strict Filter specs:", show_header=False, MessageThreadID=credentials.message_id )


DB.close_db()
