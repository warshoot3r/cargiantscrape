import sys
import os
# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



from modules.sqlite_db import SQLiteDatabase


db = SQLiteDatabase()


data = db.return_as_panda_dataframe()

db.print_as_panda_dataframe(data)