from webscrape_cargiant_class import webscrape_cargiant
from sqlite_test_db import sqlite_database

DB = sqlite_database()
DB.create_table()
#scrape BMW cars
BMWCars = webscrape_cargiant()
BMWCars.searchForManufacturer("BMW")

# import to DB

# #testing to set property
# DB.setCarProperty("RV65VDM", "Price", 6000)

#Get new data and import it into DB
print(f"Number of cars to imported -> {BMWCars.data.shape[0]}")
print(BMWCars.data)
for i in range(BMWCars.data.shape[0]):
    current_car = BMWCars.data.iloc[i]
    DB.setCarProperties(
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
    DB.import_data()

# Print DB as pandas TF

DB.prettyprint()

DB.close_db()


