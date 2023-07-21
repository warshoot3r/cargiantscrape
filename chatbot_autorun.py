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
# Filters
filters = {
   'Price': lambda x: x >= 8000 & x <=18000,
    'Mileage': lambda x: x <=80000,
    'Year': lambda x: x >= 2012,
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}

#scrape cars
def scrape_cars():
    if(DB.is_db_recently_written() and not force_scrape):
        print("Not scraping as DB written in last 10 minutes")
        time.sleep(2)
        return(False)
    CarSearch = WebScraperCargiant(driver="chrome", keepalive=True)
    CarSearch.search_for_manufacturer("BMW")
    CarSearch.search_for_manufacturer("Mercedes")
    CarSearch.print_number_of_cars()
    print(CarSearch.data.shape[0])
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
                    Reg=current_car["Reg"],
                    URL=current_car["URL"],
                    Model=current_car["Model"],
                    Mileage=current_car["Mileage"]
            )


# Output a table of data and send it


# Forever loop to poll every 60 minutes
while(True):
    scraped_cars = scrape_cars()
    import_cars(scraped_cars)
    if(DB.car_price_changed()):
        DB.open_db()
        database = DB.return_as_panda_dataframe()
        database_filtered = DB.filter_table(filters, database)
        # Sending telegram data
        bot.send_message_servername(chat_id)
        bot.send_dataframe(chat_id, database_filtered[["Price", "Model", "Mileage", "URL", "Color"]])
        bot.send_dataframe_as_file(chat_id=chat_id, file_format="csv", dataframe=database)
        # 
        DB.close_db()
    else:
        bot.send_message_servername(chat_id, "No Price changed in defined filter")
    time.sleep(60*60)