from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
import re
import time

#scrape cars
DB = SQLiteDatabase()

force_scrape = False
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



def import_cars(CarSearch):
    #Get new data and import it into DB
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


# Scrape Cars:
scraped_cars = scrape_cars()
import_cars(scraped_cars)


# Output a table of data :
filters = {
   'Price': lambda x: x >= 8000 & x <=18000,
    'Mileage': lambda x: x <=80000,
    'Year': lambda x: x >= 2012,
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) &(not model.startswith('2 Series')) &(not model.startswith("B")) #
}
database = DB.return_as_panda_dataframe()
database_filtered = DB.filter_table(filters, database)
database_filtered_reducedcol  = database_filtered[["Price", "Model", "Mileage", "URL"]]
# bot.send_dataframe(chat_id, database_filtered_reducedcol)
# bot.send_dataframe_as_file(chat_id=chat_id, file_format="csv", dataframe=database)

DB.print_as_panda_dataframe(database_filtered, col_show=["Manufacturer", "Model", "Year", "Price", "Mileage","Reg", "URL"])
DB.close_db()
    