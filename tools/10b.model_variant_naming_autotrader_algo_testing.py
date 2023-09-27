# python code to test logic names for adjusting the algorhtynm
import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from modules.autotrader_naming import autotrader_naming
from modules.sqlite_db import SQLiteDatabase





car_db = SQLiteDatabase(db_path="used_cars.db")
naming = autotrader_naming(driver="safari")
data = car_db.return_as_panda_dataframe()
# Saving the BMW models data





# ### BMW
# print(naming.get_car_models("BMW"), flush=True)

bmw_custom_data = ['1602', '1 Series', '2002', '2 Series', '2 Series Active Tourer', '2 Series Gran Coupe', '2 Series Gran Tourer', '3 Series', '3 Series Gran Turismo', '4 Series', '4 Series Gran Coupe', '5 Series', '5 Series Gran Turismo', '6 Series', '6 Series Gran Coupe', '6 Series Gran Turismo', '7 Series', '8 Series', '8 Series Gran Coupe', 'Alpina B10', 'Alpina B3', 'Alpina B4', 'Alpina B4 Gran Coupe', 'Alpina B5', 'Alpina B6', 'Alpina B8 Gran Coupe', 'Alpina D3', 'Alpina D4', 'Alpina D4 Gran Coupe', 'Alpina D5', 'Alpina Roadster', 'Alpina Unspecified Models', 'Alpina XB7', 'Alpina XD3', 'E9', 'i3', 'i4', 'i5', 'i7', 'i8', 'Isetta', 'iX', 'iX1', 'iX3', 'M2', 'M3', 'M4', 'M5', 'M6', 'M6 Gran Coupe', 'M8', 'M8 Gran Coupe', 'X1', 'X2', 'X3', 'X3 M', 'X4', 'X4 M', 'X5', 'X5 M', 'X6', 'X6 M', 'X7', 'XM', 'Z1', 'Z3', 'Z3 M', 'Z4', 'Z4 M', 'Z8']

db_bmw_models = data[data["Manufacturer"] == "BMW"]
unique_database_bmw_models = (db_bmw_models["Model"].drop_duplicates()).to_list()
print( unique_database_bmw_models, flush=True)
car_names = car_db.retrieve_db(column="Manufacturer",input_data="BMW")
model_name_index = car_db.return_as_panda_dataframe().columns.get_loc("Model")
for car in unique_database_bmw_models:
    model_name = naming.translate_modelname_to_autotrader(car_make="BMW",custom_data=bmw_custom_data, input_string=str(car))
    naming.translate_modelvariant_to_autotrader(car_model=model_name, car_make="BMW", input_string=str(car))
    #### BMW



### mercedes


# Saving the BMW models data
# print(naming.get_car_models("Mercedes-Benz"), flush=True)
mercedes_custom_data = ['190', '190 SL', '200', '220', '230', '230 SL', '250', '250 SL', '260', '280', '280 S', '280 SL', '300', '310', '320', '350 SL', '380', '400', '420', '450', '450 SL', '500', '560SL', 'A Class', 'AMG', 'AMG GT', 'AMG GT 63', 'B Class', 'C Class', 'Citan', 'CL', 'CLA Class', 'CLC Class', 'CLK', 'CLS', 'E Class', 'EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV', 'eVito', 'G Class', 'GLA Class', 'GLB Class', 'GLC Class', 'GL Class', 'GLE Class', 'GLS Class', 'Maybach GLS Class', 'Maybach S Class', 'M Class', 'R Class', 'S Class', 'SE Class', 'SEC Series', 'SLC', 'SL Class', 'SLK', 'SLR McLaren', 'SLS', 'Sprinter', 'Traveliner', 'V Class', 'Viano', 'Vito', 'X Class']
['A160', 'E220', 'A180', 'CLA', 'C350e', 'C300h', 'GLA', 'C200', 'A200', 'A250', 'C220', 'B180', 'B200', 'GLC', 'C300de', 'C250', 'C300', 'E200', 'B220', 'S350L', 'A35', 'GLE', 'E300de', 'GLB', 'EQA']

db_mercedes_models = data[data["Manufacturer"] == "Mercedes"]
unique_database_mercedes_models = (db_mercedes_models["Model"].drop_duplicates()).to_list()
car_names = car_db.retrieve_db(column="Manufacturer",input_data="Mercedes-Benz")
print( unique_database_mercedes_models, flush=True)
model_name_index = car_db.return_as_panda_dataframe().columns.get_loc("Model")
for car in unique_database_mercedes_models:
    model_name = naming.translate_modelname_to_autotrader(car_make="Mercedes",custom_data=mercedes_custom_data, input_string=str(car))
    naming.translate_modelvariant_to_autotrader(car_model=model_name, car_make="Mercedes", input_string=str(car))
####




### lexus

Lexus_custom_data = ['IS 300H', 'CT 200h', 'NX 300H', 'UX', 'ES 300h', 'RX 400h', 'RC 300h', 'RX 450h']
db_Lexus_models = data[data["Manufacturer"] == "Lexus"]
unique_database_Lexus_models = (db_Lexus_models["Model"].drop_duplicates()).to_list()
car_names = car_db.retrieve_db(column="Manufacturer",input_data="Lexus")
# print( unique_database_Lexus_models, flush=True)
model_name_index = car_db.return_as_panda_dataframe().columns.get_loc("Model")



for car in unique_database_Lexus_models:
    model_name = naming.translate_modelname_to_autotrader(car_make="Lexus",custom_data=Lexus_custom_data, input_string=str(car))
    naming.translate_modelvariant_to_autotrader(car_model=model_name, car_make="Lexus", input_string=str(car))

    


# #mercedes
# # print(naming.get_car_models(make="BMW"))
# print(naming.get_model_variant_from_model(car_model="2 Series", make="BMW"))
# # naming.translate_modelvariant_to_autotrader(car_model="2 Series", car_make="BMW", input_string="218i")

