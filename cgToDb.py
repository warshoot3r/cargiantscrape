from webscrape_cargiant_class import webscrape_cargiant
from sqlite_test_db import sqlite_database


#scrape BMW cars
BMWCars = webscrape_cargiant(manufacturer_search="BMW")



#Import to DB
print(f"Number of cars to imported -> {BMWCars.data.shape[0]}")


print(BMWCars.data.iloc[0])

    