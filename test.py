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
tb.send_dataframe(chat_id=credentials.chat_id, dataframe=data_filter[["URL", "Model", "Transmission", "Price"]], caption="ff")


# link_message = "[tf](https://www.cargiant.co.uk/car/BMW/118i/GY19NKX/)"
# text = "Click <a href='http://example.com'>here</a> to visit."
# tb.send_message(message=link_message, chat_id=credentials.chat_id, ParserType="MarkdownV2")
# tb.send_message(message=text, chat_id=credentials.chat_id, ParserType="html")
