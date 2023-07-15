from modules.sqlite_test_db import sqlite_database
from modules.webscrape_cargiant_class import webscrape_cargiant

DB = sqlite_database()
DB.create_table()

#scrape cars
CarSearch = webscrape_cargiant(driver="chrome", keepalive=True)
CarSearch.getCarMakes()
CarSearch.searchForManufacturer("BMW")
CarSearch.searchForManufacturer("Mercedes")
CarSearch.searchForManufacturer("Lexus")
CarSearch.searchForManufacturer("Honda")
CarSearch.searchForManufacturer("Volkswagen")
CarSearch.searchForManufacturer("Toyota")
CarSearch.searchForManufacturer("Ford")



# import to DB

# #testing to set property
# DB.setCarProperty("RV65VDM", "Price", 8800)

#Get new data and import it into DB
print(f"\n\nNumber of cars to imported -> {CarSearch.data.shape[0]}\n\n")

for i in range(CarSearch.data.shape[0]):
    current_car = CarSearch.data.iloc[i]
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
  
# DB.delete_manufacturer_from_table(manufacturer="Vauxhall")
# DB.delete_manufacturer_from_table(manufacturer="Peugeot")
# DB.delete_manufacturer_from_table(manufacturer="Nissan")
# DB.delete_manufacturer_from_table(manufacturer="Fiat")
# DB.delete_manufacturer_from_table(manufacturer="Suzuki")
# DB.delete_manufacturer_from_table(manufacturer="Citreon")
   
  
  
table_data = DB.exportToPDdataframe()

# Print DB as pandas TF
DB.prettyprint(panda_df=table_data)

#
adjusted_table = table_data.loc[(table_data['Year'] >= 2012) & (table_data['Doors'] == 5) & (table_data['Mileage'] <= 60000) & (table_data['Price'] <= 16000)]

# print desired
print("\n\n Table printed for desired cars")
DB.prettyprint(array_col_show=["Manufacturer","Model","Year","Price","Mileage"],panda_df=adjusted_table)
DB.close_db()