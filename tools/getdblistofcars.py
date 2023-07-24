# script.py

import sys
import os

# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.sqlite_db import SQLiteDatabase

DB = SQLiteDatabase()

export = DB.return_as_panda_dataframe()

DB.print_as_panda_dataframe(export)
