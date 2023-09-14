from modules.sqlite_db import SQLiteDatabase
from modules.webscrape_cargiant_class import WebScraperCargiant
"""
Cleans up Database of car url which don't return anything"
"""

db = SQLiteDatabase()
cg = WebScraperCargiant("Chrome", False)



all_reg = db.get_all_url()
removed_count = 0

for reg in all_reg:
    if cg.check_reg_url_alive(reg[0]):
        db.move_sold_cars_to_db(reg[0])
        removed_count+=1



print(f"Updated {removed_count} cars out of {len(all_reg)} ")


db.print_raw_data_from_sqlite_db(db.return_as_panda_dataframe())