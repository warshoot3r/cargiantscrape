from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
import re

#time script
import datetime
import sys


scheduled_time = datetime.time(20)# 8 PM
print(f"Scheduled time at {scheduled_time}")
print(f"Machine time at {datetime.datetime.now()}")
while True:
        current_time = datetime.datetime.now()
        # Calculate the time difference between local time and GMT
        time_difference = current_time - datetime.datetime.utcnow()

        # Subtract the time difference to get the GMT time
        gmt_time = current_time - time_difference

        converted_current_time = gmt_time.time()
        if converted_current_time < scheduled_time:
            print(f"Not time yet {converted_current_time}")
            sys.exit()

        else:
            print("Its time")
            print(current_time)
            break
#time script


api_token = credentials.api_token
chat_id = credentials.chat_id
message_id = credentials.message_id


bot = TelegramBot(api_token)
DB = SQLiteDatabase()

DB.update_table()
# Filters
filters = {
    'Price': lambda x: x >= 10000,
    'Price': lambda x: x <= 30000,
    'Mileage': lambda x: x <= 60000,
    'Year': lambda x: x >= 2015,
    "CarStatus": lambda x: x != "Sold",
    # No Mercedes A Classes
    # No BMW 1 Series
    # No BMW i3's
    'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"),
    'Model': lambda model: (not re.match(r"[A|1]\d+", model)) & (not model.startswith('i3')) & (not model.startswith('2 Series')) & (not model.startswith("B"))
}


# Send a zip of dataframes via telegram

database = DB.return_as_panda_dataframe()
csv_dataframe = DB.filter_table(filters, database)  # every car filtered

not_available_csv = csv_dataframe.loc[csv_dataframe['CarStatus'].str.contains(
    r'AVAILABLE|Reserved', case=True, regex=True)]  # The available cars
# The available cars
available_csv = csv_dataframe.loc[csv_dataframe['CarStatus'] == "Available"]
sold_csv = csv_dataframe.loc[csv_dataframe["CarStatus"] == "Sold"]


data_frames = [not_available_csv, available_csv, sold_csv]
file_formats = ["csv", "csv", "csv"]
captions = ["Unavailable data", "Available data", "Sold data"]
file_names = ["Unavailable", "Available", "Sold"]

bot.send_message_servername(
    chat_id=chat_id, MessageThreadID=message_id, message=": Autoscheduled Daily Report")

for items in range(3):
    bot.send_dataframe_as_file(
        chat_id=chat_id,
        file_format=file_formats[items],
        caption=captions[items],
        file_name=file_names[items],
        dataframe=data_frames[items],
        MessageThreadID=message_id
    )



# bot.send_dataframe_as_multiple_files_as_zip(
#     file_formats=file_formats,
#     captions=captions,
#     chat_id=credentials.chat_id,
#     dataframes=data_frames,
#     file_names=file_names,
#     MessageThreadID=message_id

# )
