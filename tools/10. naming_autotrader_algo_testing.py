# python code to test logic names for adjusting the algorhtynm
import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from modules.autotrader_naming import autotrader_naming
from modules.sqlite_db import SQLiteDatabase



### BMW

car_db = SQLiteDatabase(db_path="used_cars.db")
naming = autotrader_naming(driver="safari")
data = car_db.return_as_panda_dataframe()
# Saving the BMW models data
# print(naming.get_car_models("BMW"))
bmw_custom_data = ['1602', '1 Series', '2002', '2 Series', '2 Series Active Tourer', '2 Series Gran Coupe', '2 Series Gran Tourer', '3 Series', '3 Series Gran Turismo', '4 Series', '4 Series Gran Coupe', '5 Series', '5 Series Gran Turismo', '6 Series', '6 Series Gran Coupe', '6 Series Gran Turismo', '7 Series', '8 Series', '8 Series Gran Coupe', 'Alpina B10', 'Alpina B3', 'Alpina B4', 'Alpina B4 Gran Coupe', 'Alpina B5', 'Alpina B6', 'Alpina B8 Gran Coupe', 'Alpina D3', 'Alpina D4', 'Alpina D4 Gran Coupe', 'Alpina D5', 'Alpina Roadster', 'Alpina Unspecified Models', 'Alpina XB7', 'Alpina XD3', 'E9', 'i3', 'i4', 'i5', 'i7', 'i8', 'Isetta', 'iX', 'iX1', 'iX3', 'M2', 'M3', 'M4', 'M5', 'M6', 'M6 Gran Coupe', 'M8', 'M8 Gran Coupe', 'X1', 'X2', 'X3', 'X3 M', 'X4', 'X4 M', 'X5', 'X5 M', 'X6', 'X6 M', 'X7', 'XM', 'Z1', 'Z3', 'Z3 M', 'Z4', 'Z4 M', 'Z8']

db_bmw_models = data[data["Manufacturer"] == "BMW"]
unique_database_bmw_models = (db_bmw_models["Model"].drop_duplicates()).to_list()
print( unique_database_bmw_models, flush=True)
car_names = car_db.retrieve_db(column="Manufacturer",input_data="BMW")
model_name_index = car_db.return_as_panda_dataframe().columns.get_loc("Model")
for car in unique_database_bmw_models:
    naming.translate_modelname_to_autotrader(car_make="BMW",custom_data=bmw_custom_data, input_string=str(car))


#### BMW



### mercedes


# Saving the BMW models data
print(naming.get_car_models("Mercedes-Benz"))
db_bmw_models = data[data["Manufacturer"] == "Mercedes"]
unique_database_bmw_models = (db_bmw_models["Model"].drop_duplicates()).to_list()
print( unique_database_bmw_models, flush=True)
car_names = car_db.retrieve_db(column="Manufacturer",input_data="Mercedes-Benz")
model_name_index = car_db.return_as_panda_dataframe().columns.get_loc("Model")
for car in unique_database_bmw_models:
    naming.translate_modelname_to_autotrader(car_make="Mercedes",custom_data=bmw_custom_data, input_string=str(car))




#mercedes