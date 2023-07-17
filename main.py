from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
import re

#scrape cars
def scrape_cars():
    CarSearch = WebScraperCargiant(driver="chrome", keepalive=True)
    CarSearch.search_for_manufacturer("BMW")
    CarSearch.search_for_manufacturer("Mercedes")
    CarSearch.print_number_of_cars()
    print(CarSearch.data.shape[0])
    return CarSearch



def import_cars(CarSearch):
    #Get new data and import it into DB
    for i in range(CarSearch.length):
        current_car = CarSearch.data.iloc[i]
        print(current_car["Reg"])
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



DB = SQLiteDatabase()


# scraped_cars = scrape_cars()
# import_cars(scraped_cars)


filters = {
   'Price': lambda x: x >= 8000 & x <=18000,
    'Mileage': lambda x: x <=70000,
    'Year': lambda x: x >= 2012,
     # No Mercedes A Classes 
     # No BMW 1 Series
     # No BMW i3's
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) #
}

database = DB.return_as_panda_dataframe()
database = DB.filter_table(filters, database)

DB.print_as_panda_dataframe(database, col_show=["Manufacturer", "Model", "Year", "Price", "Mileage","Reg", "URL"])



DB.close_db()
    