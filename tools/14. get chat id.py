import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
DB = SQLiteDatabase()
tb = TelegramBot(api_token=credentials.api_token)

tb.get_updates()


# link_message = "[tf](https://www.cargiant.co.uk/car/BMW/118i/GY19NKX/)"
# text = "Click <a href='http://example.com'>here</a> to visit."
# tb.send_message(message=link_message, chat_id=credentials.chat_id, ParserType="MarkdownV2")
# tb.send_message(message=text, chat_id=credentials.chat_id, ParserType="html")
