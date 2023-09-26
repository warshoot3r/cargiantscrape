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


picture = cg.get_car_url_snapshot(url="https://www.cargiant.co.uk/car/BMW/520D/KM19RUO")


bot.send_base64picture(chat_id=credentials.chat_id, base64_data=picture) 