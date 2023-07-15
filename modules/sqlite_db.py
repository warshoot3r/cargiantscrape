import sqlite3
import datetime
import pandas as pd

class sqlite_database():
    

    def __init__(self):
        self.conn = sqlite3.connect('used_cars.db')
        self.cursor = self.conn.cursor()


    def setCarProperties(self, Manufacturer=None, Doors=None, Model=None, Year=None, Price=None, Body_Type=None, Transmission=None, Fuel=None, Color=None, Mileage=None, Reg=None, URL=None):
        # Define instance variables
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
    def setCarProperty(self, REG, Key, Value):
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
    # Create a table to store used car information if it doesn't exist
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
        sql_table_col =  ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])
        sql_string = f'''CREATE TABLE IF NOT EXISTS {sql_table}
                        (id INTEGER PRIMARY KEY,
                        {sql_table_col}
                        )
        '''
        
        self.cursor.execute(sql_string)
    def delete_data_from_table(self, REG, table=None):
        # Generate the column number
        table = "used_cars"

        print(f"deleting {REG} from {table}")

        sql_string = f"DELETE FROM {table} where Reg = '{REG}' "
        self.cursor.execute(sql_string)
        self.conn.commit()
    def delete_manufacturer_from_table(self, manufacturer, table=None):
        # Generate the column number
        table = "used_cars"

        print(f"deleting {manufacturer} from {table}")

        sql_string = f"DELETE FROM {table} where Manufacturer = '{manufacturer}' "
        self.cursor.execute(sql_string)
        self.conn.commit()

    def exportToPDdataframe(self):
        query = "SELECT * from used_cars"
        return pd.read_sql(query, self.conn)
    
    def prettyprint(self,panda_df, array_col_show=None ):
        table = panda_df #¢self.exportToPDdataframe()
        sorted_table = table.sort_values(by="Price")
        pd.set_option('display.max_rows', None)
        if(array_col_show):
            print(sorted_table[[*array_col_show]])
        else:
            print(sorted_table)

    # Print all information from the 'used_cars' table
    def print_all_table(self):
        """
        Prints all the data in the 'used_cars' table.
        """
        print("Printing table information:")
        self.cursor.execute("SELECT * from used_cars")
        for item in self.cursor.fetchall():
            print(item)

    def import_data(self): #Inport from instance variables

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
        self.cursor.execute("select * from used_cars")# Improvement to add table by date
        existing_data = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        reg_col_index = column_names.index('Reg')
        
        for data in incoming_data:
            matching_car = next((car for car in existing_data if (car[reg_col_index]) == (data["Reg"])), None)
            if(matching_car):
                self.cursor.execute(f"SELECT Price FROM used_cars where Reg = '{matching_car[reg_col_index]}'")
                car_DB_PRICE = (self.cursor.fetchall())[0][0]
                Car_Current_price = self.Price
                print(f"Car with Reg: {matching_car[reg_col_index]} is existing with same price")
                if(Car_Current_price != car_DB_PRICE):
                    print("Car Price Changed, updating DB.")
                    self.DateUpdated = datetime.datetime.now()
                    print(f"DatabasePrice={car_DB_PRICE} CurrentPrice={Car_Current_price}")
                    table = "used_cars"
                    car_properties = incoming_data[0]
                    car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                    sql_values_count_string = ", ".join([f"?" for _  in car_properties])
            
                    db_string = f'''
                    UPDATE {table} SET OldPrice = ?,Price = ?,OldDate = DateUpdated, DateUpdated = ? WHERE Reg = '{matching_car[reg_col_index]}'
                    '''
                    print(self.DateUpdated)
                    self.cursor.execute(db_string, (car_DB_PRICE, Car_Current_price, self.DateUpdated ) )
                    self.conn.commit()
                    print("Imported updated entry")


            else: # Add a new car into database
                print(f"Adding a new Car into the DB: '{data['Reg']}'")
                table = "used_cars"
                car_properties = incoming_data[0]
                car_properties_keys = ", ".join([f'"{key}"' for key, values in incoming_data[0].items()])

                sql_values_count_string = ", ".join([f"?" for _  in car_properties])
        
                db_string = f"INSERT INTO {table} ({car_properties_keys}) VALUES({sql_values_count_string})"

                self.cursor.execute(db_string, (*car_properties.values(),) )
                self.conn.commit()

    def retrieve_db(self, column, input_data):
        if(column == "price"): # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif(column == "mileage"): # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif(column == "year"): # For integer col
            command = f"SELECT * from used_cars where {column} <= {input_data} "
        elif(column == "doors"): # For integer col
            command = f"SELECT * from used_cars where {column} = {input_data} "
        else: #For strings
            command = f"SELECT * from used_cars where {column} LIKE '{input_data}' "
        print(command)
        self.cursor.execute(command)
        data = self.cursor.fetchall()
     
        print(f"\nPrinting data from query: {column} -> {input_data}")
        for item in data: print(item)


    # Close the database connection and cursor
    def close_db(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.conn.close()


# Main program execution
# batchofcarsimport = sqlite_database(
#     Body_Type="Hatch",
#     Color="Black",
#     Fuel="Diesel",
#     Doors=5,
#     Manufacturer="Ford",
#     Mileage=66000,
#     Model="Fiesta",
#     Price=12000,
#     Reg="2mk60g22",
#     Year=2017,
#     Transmission="Manual",
#     URL="www.google.com"
# )
# batchofcarsimporttest = sqlite_database(
#     Body_Type="Hatch",
#     Color="Black",
#     Fuel="Diesel",
#     Doors=5,
#     Manufacturer="Ford",
#     Mileage=66000,
#     Model="Focus",
#     Price=12000,
#     Reg="2mk60g22",
#     Year=2017,
#     Transmission="Manual",
#     URL="www.google.com"
# )

# batchofcarsimport.create_table()  # Create the 'used_cars' table if it doesn't exist
# #Import car data
# batchofcarsimport.import_data()
# batchofcarsimporttest.import_data()





# batchofcarsimport.retrieve_db(column="price", input_data=100000)
# batchofcarsimport.retrieve_db(column="color", input_data='black')
# batchofcarsimport.retrieve_db(column="doors", input_data='5')


# batchofcarsimport.close_db()  # Close the database connection and cursor