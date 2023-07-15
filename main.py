from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant


#scrape cars
def scrape_cars():
    CarSearch = WebScraperCargiant(driver="chrome", keepalive=True)
    CarSearch.search_for_manufacturer("BMW")
    CarSearch.search_for_manufacturer("Mercedes")
    #Get new data and import it into DB
    CarSearch.print_number_of_cars()
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
    
def print_data():
# Print DB as pandas TF
    table_data = DB.export_to_pd_dataframe()
    DB.pretty_print(panda_df=table_data)
    adjusted_table = table_data.loc[(table_data['Year'] >= 2012) & (table_data['Doors'] == 5) & (table_data['Mileage'] <= 60000) & ((table_data['Price'] <= 16000) & (table_data['Price'] >= 8000))]
    # print desired
    print("\n\n Table printed for desired cars")
    DB.pretty_print(col_show=["Manufacturer","Model","Year","Price","Mileage","URL"],panda_df=adjusted_table)
    DB.close_db()

DB = SQLiteDatabase()
scrape_cars()
print_data()