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
        self.open_db()
        self.create_table()
        self.number_of_car_prices_changed = 0
        self.number_of_car_new_changed = 0
        self.number_of_car_status_changed = 0
        self.number_of_car_prices_changed_list = [] # Stores the REG of price changed vehicles
        self.number_of_car_new_changed_list = [] # Stores the REG of new vehicles
        self.number_of_car_status_changed_list = []
    def open_db(self):
        """
        Connects to the local DB file
        """
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

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



    def import_car_properties(self, Manufacturer=None, Doors=None, Model=None, Year=None, Price=None, Body_Type=None, Transmission=None, Fuel=None, Color=None, Mileage=None, Reg=None, URL=None, CarStatus=None):
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
        self.CarStatus = str(CarStatus)
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
                "OldDate": "TEXT",
                "NumberOfPriceReductions": "INTEGER",
                "CarStatus": "TEXT",
                "NumberReserved": "INTEGER"
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

    def update_table(self):
        """
        Update tables if the schema is changed
        """
        schema =      {
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
                "OldDate": "TEXT",
                "NumberOfPriceReductions": "INTEGER",
                "CarStatus": "TEXT",
                "NumberReserved": "INTEGER"
            }
        # Get current tables column
        table_name = "used_cars"
        self.cursor.execute("PRAGMA table_info({});".format(table_name) )
        columns = self.cursor.fetchall()

        for missingcolumn in schema:
            column_to_update = any(column[1] == missingcolumn for column in columns  )
            if not column_to_update:
                print(f"Missing {missingcolumn} in DB. Database is being updated with table")
                db_string = '''
                ALTER TABLE {}
                ADD {}
                '''
                self.cursor.execute(db_string.format(table_name, missingcolumn))
                print("DB updated")
        else:
            print("No changes needed")
        

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
    
    def filter_table(self, filters, db, ListOfCarRegistrations=None):
        """
        Function to filter a datafram by lambda expressions and via a list of REG
        """
        combined_filters = []
        for column, condition in filters.items():
            combined_filters.append(db[column].apply(condition))

        database = db[reduce(lambda x, y: x & y, combined_filters)]
   
        if ListOfCarRegistrations != None:
            combined_filters_reg = [] 
            for current_reg in ListOfCarRegistrations:
                combined_filters_reg.append(db["Reg"].map(lambda x : x == current_reg)) 
            filtered_and_reg_database = db[reduce(lambda x, y: x | y , combined_filters_reg)]
        
            return filtered_and_reg_database.sort_values(by="Price")

        else:
            return database.sort_values(by="Price")

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

    def get_car_sold_as_pd(self):
        sqlstring = """
        SELECT * FROM used_cars where CarStatus LIKE 'Sold';    
        """
        data = pd.read_sql_query(sqlstring, self.conn)
        return data.sort_values(by="Price")


    def car_status_changed(self):
        """
        Return number of cars status changed
        """
        if(self.number_of_car_status_changed == 0):
            return False
        else: 
            print("Car Status Changed")
            value = self.number_of_car_status_changed
            self.number_of_car_status_changed = 0
            return value
    def get_car_status_changed(self):
        """
        Return status of cars changed
        """
        data = self.number_of_car_status_changed_list
        self.number_of_car_status_changed_list = []
        return data
    def car_price_changed(self):
        """
         Return the number of cars
        """
        if(self.number_of_car_prices_changed == 0):
            return False
        else:
            print("Car Prices Changed")
            value = self.number_of_car_prices_changed
            self.number_of_car_prices_changed = 0
            return value
    def car_new_changed(self):
        """
        Return the number of cars
        """
        if(self.number_of_car_new_changed == 0):
            return False
        else: 
            print("New cars were added") 
            value = self.number_of_car_new_changed
            self.number_of_car_new_changed = 0
            return value
        
    def get_car_price_changed(self):
        """
        Return list of price changed cars.
        """
        data = self.number_of_car_prices_changed_list
        self.number_of_car_prices_changed_list = []
        return data
    def get_car_new_changed(self):
        """
        Return list of new cars added.
        """
        data = self.number_of_car_new_changed_list
        self.number_of_car_new_changed_list = []
        return data
    def import_data(self):
            """
            Imports the car properties from the instance variables and adds them to the database.
            """
            #Variable to hold the price changes for reports
  
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
                    "DateUpdated": self.DateUpdated,
                    "CarStatus": self.CarStatus,
                    "NumberOfPriceReductions": 0,
                    "NumberReserved": 0
                },
            ]
            self.cursor.execute("SELECT * from used_cars")
            existing_data = self.cursor.fetchall()
            column_names = [description[0] for description in self.cursor.description]
            reg_col_index = column_names.index('Reg')

            for data in incoming_data:
                matching_car = next((car for car in existing_data if car[reg_col_index] == data["Reg"]), None)
                if matching_car:
                    currentcarreg = matching_car[reg_col_index] 
                    self.cursor.execute(f"SELECT Price FROM used_cars where Reg = '{currentcarreg}'")
                    car_DB_PRICE = (self.cursor.fetchall())[0][0]
                    Car_Current_price = self.Price
                    Car_Current_Status = self.CarStatus
                    self.cursor.execute(f"SELECT CarStatus FROM used_cars where Reg = '{currentcarreg}'")
                    Car_DB_Status = (self.cursor.fetchall()[0][0])
                    print(f"Car with Reg: {currentcarreg} is existing with the same price")
                    if Car_Current_price != car_DB_PRICE:
                        self.DateUpdated = datetime.datetime.now()
                        string_updated = f"Car Price Changed, updating DB. DatabasePrice={ car_DB_PRICE} CurrentPrice= {Car_Current_price}"
                        self.number_of_car_prices_changed += 1
                        self.number_of_car_prices_changed_list.append(currentcarreg) # Store the REG of price changed car in a list
                        print(string_updated)
                        table = "used_cars"
                        car_properties = incoming_data[0]
                        car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                        sql_values_count_string = ", ".join([f"?" for _ in car_properties])

                        db_string = f'''
                        UPDATE {table} SET OldPrice = ?, Price = ?, OldDate = DateUpdated, DateUpdated = ?, NumberOfPriceReductions = NumberOfPriceReductions + 1 WHERE Reg = ?
                        '''
                        print(self.DateUpdated)
                        self.cursor.execute(db_string, (car_DB_PRICE, Car_Current_price, self.DateUpdated, currentcarreg))
                        self.conn.commit()
                        print("Imported updated entry")
                    if Car_Current_Status != Car_DB_Status:
                        self.number_of_car_status_changed_list.append(currentcarreg)
                        self.number_of_car_status_changed += 1
                        table = "used_cars"
                        string_updated = f"Car status changed for {currentcarreg}. Old status:{Car_DB_Status}. New Status: {self.CarStatus}"
                        print(string_updated)
                        db_string = f'''
                        UPDATE {table} SET CarStatus = ? WHERE REG = ?
                        '''
                        if Car_Current_price == "Reserved":
                            db_string = f'''
                             UPDATE {table} SET CarStatus = ?, NumberReserved = NumberReserved + 1 WHERE REG = ?
                               '''
                            print("Car was reserved so incrementing the count NumberReserved")
                        self.cursor.execute(db_string, (self.CarStatus, currentcarreg))
                        self.conn.commit()    

                else:  # Add a new car into the database
                    print(f"Adding a new Car into the DB: {data['Reg']}. The car is a {data['Manufacturer']} {data['Model']} with {data['Mileage']} miles.")
                    table = "used_cars"
                    self.number_of_car_new_changed += 1
                    self.number_of_car_new_changed_list.append(data['Reg']) # Store the REG of new car in a list
                    car_properties = incoming_data[0]
                    car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                    sql_values_count_string = ", ".join([f"?" for _ in car_properties])

                    db_string = f"INSERT INTO {table} ({car_properties_keys}) VALUES({sql_values_count_string})"

                    self.cursor.execute(db_string, (*car_properties.values(),))
                    self.conn.commit()
    def move_sold_cars_to_db():
        """
        Moves the "Sold" cars to a different table and deletes it from database

        Args:
            Optional Db_File. defaults to used_cars_sold.db

        """

        pass