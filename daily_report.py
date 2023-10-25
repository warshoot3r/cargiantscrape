from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
from modules.telegram_bot import TelegramBot
import credentials
import re

#time script
import datetime
import sys


scheduled_time_start_hour = 20
scheduled_time_end_hour = 21

print(f"Scheduled time is {scheduled_time_start_hour}:00 to {scheduled_time_end_hour}:00. Machine time -> {datetime.datetime.now().strftime('%H:%M')}")
while True:
        current_time = datetime.datetime.now()
        # Calculate the time difference between local time and GM
        time_str = current_time.strftime('%H:%M')
        if  scheduled_time_start_hour <= current_time.hour < scheduled_time_end_hour:

            print(f"It's time {time_str}", flush=True)
            break

        else:
            print(f"Not time. Cancelling {time_str}", flush=True)
            sys.exit()

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
    "Engine Size": lambda x: x > "1.5",
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


sold_csv = database.loc[database['CarStatus'] == "Sold"]

print(csv_dataframe, flush=True)

data_frames = [not_available_csv, available_csv, sold_csv]
file_formats = ["csv", "csv", "csv"]
captions = ["Unavailable data", "Available data", "Sold data"]
file_names = ["Unavailable", "Available", "Sold"]

bot.send_message_servername(
    chat_id=chat_id, MessageThreadID=message_id, message=": Autoscheduled Daily Report")


cars_of_the_day_filters = {
    'Price': lambda x : 9500 <= x <= 15000,
    'Year': lambda x: x >= 2018,
    'DaysAdded': lambda x: x <= 10,
    'Transmission': lambda x: x == 'Auto',
    'Engine Size': lambda x: x >= '1.5',
    'Body Type': lambda bodytype: bodytype not in ("Estate", "SUV"),
    "CarStatus": lambda x: x == "Available",
    'Mileage': lambda x: x <= 60000,
    'Model': lambda model: (not model.startswith("B"))


}

cars_of_the_day = DB.filter_table(db=database, filters=cars_of_the_day_filters)

print(cars_of_the_day, flush=True)
bot.send_dataframe_as_file(caption="Suggested Cars of the Day",chat_id=credentials.chat_id, file_format='csv', dataframe=cars_of_the_day,file_name="cotd",MessageThreadID=message_id )
# send seperate csv files

# for items in range(3):
#     bot.send_dataframe_as_file(
#         chat_id=chat_id,
#         file_format=file_formats[items],
#         caption=captions[items],
#         file_name=file_names[items],
#         dataframe=data_frames[items],
#         MessageThreadID=message_id
#     )



bot.send_dataframe_as_multiple_files_as_zip(
    file_formats=file_formats,
    captions=captions,
    chat_id=credentials.chat_id,
    dataframes=data_frames,
    file_names=file_names,
    MessageThreadID=message_id

)
