from webscrape_cargiant_class import webscrape_cargiant
from sqlite_test_db import sqlite_database


#scrape BMW cars
BMWCars = webscrape_cargiant(manufacturer_search="BMW")


DB = sqlite_database()

# import to DB
DB.create_table()
print(f"Number of cars to imported -> {BMWCars.data.shape[0]}")
print(BMWCars.data)
for i in range(BMWCars.data.shape[0]):
    current_car = BMWCars.data.iloc[i]
    print(f"Imported {current_car.Reg}")
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

DB.print_all_table()

DB.close_db()
    