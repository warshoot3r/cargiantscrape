import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
from modules.background_pricecheck import car, car_background_information
from modules.autotrader_naming import autotrader_naming


naming = autotrader_naming(driver='chrome')

custom_data = ['190', '190 SL', '200', '220', '230', '230 SL', '250', '250 SL', '260', '280', '280 S', '280 SL', '300', '310', '320', '350 SL', '380', '400', '420', '450', '450 SL', '500', '560SL', 'A Class', 'AMG', 'AMG GT', 'AMG GT 63', 'B Class', 'C Class', 'Citan', 'CL', 'CLA Class', 'CLC Class', 'CLK', 'CLS', 'E Class', 'EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV', 'eVito', 'G Class', 'GLA Class', 'GLB Class', 'GLC Class', 'GL Class', 'GLE Class', 'GLS Class', 'Maybach GLS Class', 'Maybach S Class', 'M Class', 'R Class', 'S Class', 'SE Class', 'SEC Series', 'SLC', 'SL Class', 'SLK', 'SLR McLaren', 'SLS', 'Sprinter', 'Traveliner', 'V Class', 'Viano', 'Vito', 'X Class']

# mercedes_models = naming.get_car_models(make="Mercedes-Benz")
# print(mercedes_models)

test_items =["GLE", "GLA", "GLC", "GLB"]

for items in test_items:
    (naming.translate_modelname_to_autotrader(car_make="Mercedes", custom_data=custom_data, input_string=items))
    print("\n")
