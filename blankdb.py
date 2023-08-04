from modules.sqlite_db import SQLiteDatabase


# Init
DB = SQLiteDatabase()

data = DB.get_car_sold_as_pd()

print(data)