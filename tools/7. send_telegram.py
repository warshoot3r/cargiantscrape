import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.telegram_bot import TelegramBot
import credentials

bot = TelegramBot(api_token=credentials.api_token)

bot.get_updates()
bot.send_message_servername(chat_id=credentials.chat_id, message="test")