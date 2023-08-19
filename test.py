from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot


#Create DB 
DB = SQLiteDatabase()

#create Telegrambot
tb = TelegramBot(api_token=33)


data = DB.return_as_panda_dataframe()

#Create selenium
cars = WebScraperCargiant(driver="chrome", keepalive=True)

# test 1
cars.get_car_makes()


#test 2
filter = {

    'Price': lambda x: x >= 17000
    }
array = ["MF68CEX", "YK16ETD", "YH16JUK"]
data_filter = DB.filter_table( filter, data, array)

print("Successful execution")