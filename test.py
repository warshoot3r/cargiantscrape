from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
DB = SQLiteDatabase()
tb = TelegramBot(api_token=credentials.api_token)

data = DB.return_as_panda_dataframe()
cars = WebScraperCargiant(driver="chrome", keepalive=True)


filter = {

    'Price': lambda x: x >= 17000
    }
array = ["MF68CEX", "YK16ETD", "YH16JUK"]
data_filter = DB.filter_table( filter, data, array)
print(data_filter)
tb.send_dataframe(chat_id=credentials.chat_id, dataframe=data_filter[[ "URL", "CarStatus", "Price", "NumberReserved"]])



