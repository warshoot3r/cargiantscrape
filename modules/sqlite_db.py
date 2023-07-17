import sqlite3
import datetime
import pandas as pd
from functools import reduce

class SQLiteDatabase:
    """
    A class for managing a SQLite database for used car information.
    """

    def __init__(self):
        """
        Initializes the SQLiteDatabase object by establishing a connection to the database and creating the 'used_cars' table if it doesn't exist.
        """
        self.conn = sqlite3.connect('used_cars.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    # Rest of the class methods...

    def return_as_panda_dataframe(self):
        """
        Reads the data from the 'used_cars' table into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the 'used_cars' table.
        """
        sql_query = "SELECT * from used_cars"
        data = pd.read_sql(sql_query, self.conn)
        return data

    def filter_table(self, filters):
        """
        Filters the data in the 'used_cars' table based on specified filters.

        Args:
            filters (dict): A dictionary of column names and corresponding filter functions to apply.

        Returns:
            pandas.DataFrame: A DataFrame containing the filtered data.
        """
        combined_filters = []
        for column, condition in filters.items():
            combined_filters.append(self.data[column].apply(condition))
        self.data = self.data[reduce(lambda x, y: x & y, combined_filters)]
        return self.data

    def print_as_panda_dataframe(self, table, col_show=None):
        """
        Prints a formatted representation of the DataFrame.

        Args:
            table (pandas.DataFrame): The DataFrame to be displayed.
            col_show (list, optional): The list of column names to be displayed. Defaults to None.
        """
        sorted_table = table.sort_values(by="Price")
        pd.set_option('display.max_rows', None)
        if col_show:
            print(sorted_table[[*col_show]])
        else:
            print(sorted_table)

    def retrieve_db(self, column, input_data):
        """
        Retrieves car data from the database based on the specified column and input data.

        Args:
            column (str): The column name to search for data.
            input_data (str/int): The input data to be searched.
        """
        if column in ["price", "mileage", "year", "doors"]:  # For integer columns
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        else:  # For string columns
            command = f"SELECT * from used_cars where {column} LIKE '{input_data}' "
        print(command)
        self.cursor.execute(command)
        data = self.cursor.fetchall()

        print(f"\nPrinting data from query: {column} -> {input_data}")
        for item in data:
            print(item)

    def close_db(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.conn.close()

# Rest of the class implementation...
