import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.telegram_bot import TelegramBot
import credentials

bot = TelegramBot(api_token=credentials.api_token)

bot.get_recent_messages()
bot.get_updates()



bot.send_message(chat_id=credentials.cargiant_group_chat_id, message="test to testing chat", MessageThreadID=credentials.cargiant_testing_message_id)

bot.send_message(chat_id=credentials.cargiant_group_chat_id, message="test to general chat", MessageThreadID=credentials.cargiant_general_id)

bot.send_message(chat_id=credentials.cargiant_group_chat_id, message="test to production chat", MessageThreadID=credentials.cargiant_production_id)
