import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
import re
import time


# Init
force_scrape = True

api_token = credentials.api_token
chat_id = credentials.chat_id

bot = TelegramBot(api_token)
DB = SQLiteDatabase()
cg = WebScraperCargiant(driver="chrome", keepalive=False)

urls = DB.get_all_url()

# picture = cg.get_car_url_snapshot(url="https://www.cargiant.co.uk/car/BMW/330e/RO18UTU")
# bot.send_base64picture(chat_id=credentials.chat_id, message_id=credentials.cargiant_testing_message_id, base64_data=picture) 



url = urls[:5]
print(url)
picture = cg.get_car_url_snapshot(url=url)
bot.send_base64pictures(chat_id=credentials.chat_id, message_id=credentials.cargiant_testing_message_id, base64_data=picture) 