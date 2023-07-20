import sqlite3
import datetime
from functools import reduce
import pandas as pd
import os

class SQLiteDatabase:
    """
    A class for managing a SQLite database for used car information.
    """

    def __init__(self, db_path=None):
        """
        Initializes the SQLiteDatabase object by establishing a connection to the database and creating the 'used_cars' table if it doesn't exist.
        """
        if db_path == None:
            self.db_path = "used_cars.db"
        else:
            self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()


    def get_db_last_write_time(self):
        """
        Gets the database file last write time as a date.
        """
        try:
            last_write_time = os.path.getmtime(self.db_path)
            return datetime.datetime.fromtimestamp(last_write_time)
        except FileNotFoundError:
            return None
    
    def write_empty_data(self):
        """
        Write empty string to timestamp table. This is to increment the modified time for is_db_recently_written
        """
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS timestamp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
            )
            ''')
        self.cursor.execute('INSERT INTO timestamp (data) VALUES (?)', [''])
        self.conn.commit()
        self.conn.close()

    def is_db_recently_written(self, max_time_difference=600):
        """
        Returns True if DB was last written in 10 minutes.
        """
        last_db_write_time = self.get_db_last_write_time()
        if last_db_write_time is not None:
            current_time = datetime.datetime.now()
            time_difference = current_time - last_db_write_time
            if time_difference.total_seconds() <= max_time_difference:
                return True
            else:
                self.write_empty_data()
                return False
        else:
            # If last_db_write_time is None, the database has never been written before.
            return False



    def import_car_properties(self, Manufacturer=None, Doors=None, Model=None, Year=None, Price=None, Body_Type=None, Transmission=None, Fuel=None, Color=None, Mileage=None, Reg=None, URL=None):
        """
        Imports car properties and adds them to the database.
        
        Args:
            Manufacturer (str): The manufacturer of the car.
            Doors (int): The number of doors of the car.
            Model (str): The model of the car.
            Year (int): The year of the car.
            Price (int): The price of the car.
            Body_Type (str): The body type of the car.
            Transmission (str): The transmission type of the car.
            Fuel (str): The fuel type of the car.
            Color (str): The color of the car.
            Mileage (int): The mileage of the car.
            Reg (str): The registration number of the car.
            URL (str): The URL of the car's listing.
        """
        self.Manufacturer = str(Manufacturer)
        self.Model = str(Model)
        self.Year = int(Year)
        self.Price = int(Price)
        self.Body_Type = str(Body_Type)
        self.Transmission = str(Transmission)
        self.Fuel = str(Fuel)
        self.Color = str(Color)
        self.Mileage = int(Mileage)
        self.OldPrice = 0
        try:
            self.Doors = int(Doors)
        except ValueError:
            self.Doors = "N/A"
        self.Reg = str(Reg)
        self.URL = str(URL)
        self.DateUpdated = datetime.datetime.now()
        self.import_data()


    def set_car_db_property(self, REG, Key, Value):
        """
        Sets a specific property of a car in the database.
        
        Args:
            REG (str): The registration number of the car.
            Key (str): The property key to be updated.
            Value (str): The new value of the property.
        """
        sql_string_select = f'''
            SELECT * from used_cars where Reg = '{REG}'
            '''
        self.cursor.execute(sql_string_select)
        car_data = self.cursor.fetchall()
        print(f"Old Data is {car_data}")
        sql_string_update = f'''
            UPDATE used_cars SET {Key} = ? WHERE Reg = '{REG}'
            '''
        self.cursor.execute(sql_string_update, (Value,))
        self.cursor.execute(sql_string_select)
        car_data = self.cursor.fetchall()
        print(f"New Data is {car_data}")

    def create_table(self):
        """
        Creates the 'used_cars' table if it doesn't exist.
        The table has columns: id, make, model, and price.
        """
        incoming_data = [
            {
                "Manufacturer": "TEXT",
                "Model": "TEXT",
                "Year": "INTEGER",
                "Price": "INTEGER",
                "Body Type": 'TEXT',
                "Transmission": "TEXT",
                "Fuel": "TEXT",
                "Color": "TEXT",
                "Mileage": "INTEGER",
                "Doors": "INTEGER",
                "Reg": "TEXT",
                "URL": "TEXT",
                "DateUpdated": "TEXT",
                "OldPrice": "INTEGER",
                "OldDate": "TEXT"
            }
        ]
        sql_table = "used_cars"
        sql_table_col = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])
        sql_string = f'''CREATE TABLE IF NOT EXISTS {sql_table}
                        (id INTEGER PRIMARY KEY,
                        {sql_table_col}
                        )
        '''
        self.cursor.execute(sql_string)

    def delete_car_from_table(self, REG, table=None):
        """
        Deletes a specific car's data from the database.
        
        Args:
            REG (str): The registration number of the car to be deleted.
            table (str, optional): The table name. Defaults to None.
        """
        table = "used_cars"

        print(f"deleting {REG} from {table}")

        sql_string = f"DELETE FROM {table} where Reg = '{REG}' "
        self.cursor.execute(sql_string)
        self.conn.commit()

    def delete_manufacturer_from_table(self, manufacturer, table=None):
        """
        Deletes all cars of a specific manufacturer from the database.
        
        Args:
            manufacturer (str): The manufacturer to be deleted.
            table (str, optional): The table name. Defaults to None.
        """
        table = "used_cars"

        print(f"deleting {manufacturer} from {table}")

        sql_string = f"DELETE FROM {table} where Manufacturer = '{manufacturer}' "
        self.cursor.execute(sql_string)
        self.conn.commit()
    
    def return_as_panda_dataframe(self):
        """
        Reads the data from the 'used_cars' table into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the 'used_cars' table.
        """
        sql_query = "SELECT * from used_cars"
        data = pd.read_sql(sql_query, self.conn)
        return data
    
    def filter_table(self, filters, db):

        combined_filters = []
        for column, condition in filters.items():
            combined_filters.append(db[column].apply(condition))

        database = db[reduce(lambda x, y: x & y, combined_filters)]

        return database

    def print_as_panda_dataframe(self, table, col_show=None, ):
        """
        Returns a formatted representation of the DataFrame.
        
        Args:
            col_show (list, optional): The list of column names to be displayed. Defaults to None.
        """

        sorted_table = table.sort_values(by="Price")
        pd.set_option('display.max_rows', None)
        if col_show:
            print(sorted_table[[*col_show]])
        else:
            print(sorted_table)

    def print_raw_data_from_sqlite_db(self):
        """
        Prints all the data in the 'used_cars' table.
        """
        print("Printing table information:")
        self.cursor.execute("SELECT * from used_cars")
        self.conn.commit()
        for item in self.cursor.fetchall():
            print(item)

  
    def retrieve_db(self, column, input_data):
        """
        Retrieves car data from the database based on the specified column and input data.
        
        Args:
            column (str): The column name to search for data.
            input_data (str/int): The input data to be searched.
        """
        if column == "price":  # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif column == "mileage":  # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif column == "year":  # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif column == "doors":  # For integer col
            command = f"SELECT * from used_cars where {column} = {input_data} "
        else:  # For strings
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
    def import_data(self):
            """
            Imports the car properties from the instance variables and adds them to the database.
            """
            incoming_data = [
                {
                    "Manufacturer": self.Manufacturer,
                    "Model": self.Model,
                    "Year": self.Year,
                    "Price": self.Price,
                    "Body Type": self.Body_Type,
                    "Transmission": self.Transmission,
                    "Fuel": self.Fuel,
                    "Color": self.Color,
                    "Mileage": self.Mileage,
                    "Doors": self.Doors,
                    "Reg": self.Reg,
                    "URL": self.URL,
                    "OldPrice": self.OldPrice,
                    "DateUpdated": self.DateUpdated
                }
            ]
            self.cursor.execute("SELECT * from used_cars")
            existing_data = self.cursor.fetchall()
            column_names = [description[0] for description in self.cursor.description]
            reg_col_index = column_names.index('Reg')

            for data in incoming_data:
                matching_car = next((car for car in existing_data if car[reg_col_index] == data["Reg"]), None)
                if matching_car:
                    self.cursor.execute(f"SELECT Price FROM used_cars where Reg = '{matching_car[reg_col_index]}'")
                    car_DB_PRICE = (self.cursor.fetchall())[0][0]
                    Car_Current_price = self.Price
                    print(f"Car with Reg: {matching_car[reg_col_index]} is existing with the same price")
                    if Car_Current_price != car_DB_PRICE:
                        print("Car Price Changed, updating DB.")
                        self.DateUpdated = datetime.datetime.now()
                        print(f"DatabasePrice={car_DB_PRICE} CurrentPrice={Car_Current_price}")
                        table = "used_cars"
                        car_properties = incoming_data[0]
                        car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                        sql_values_count_string = ", ".join([f"?" for _ in car_properties])

                        db_string = f'''
                        UPDATE {table} SET OldPrice = ?, Price = ?, OldDate = DateUpdated, DateUpdated = ? WHERE Reg = '{matching_car[reg_col_index]}'
                        '''
                        print(self.DateUpdated)
                        self.cursor.execute(db_string, (car_DB_PRICE, Car_Current_price, self.DateUpdated))
                        self.conn.commit()
                        print("Imported updated entry")

                else:  # Add a new car into the database
                    print(f"Adding a new Car into the DB: {data['Reg']}. The car is a {data['Manufacturer']} {data['Model']} with {data['Mileage']} miles.")
                    table = "used_cars"
                    car_properties = incoming_data[0]
                    car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                    sql_values_count_string = ", ".join([f"?" for _ in car_properties])

                    db_string = f"INSERT INTO {table} ({car_properties_keys}) VALUES({sql_values_count_string})"

                    self.cursor.execute(db_string, (*car_properties.values(),))
                    self.conn.commit()
