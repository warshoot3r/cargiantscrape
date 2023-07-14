import sqlite3


class sqlite_database():
    conn = sqlite3.connect('used_cars.db')
    cursor = conn.cursor()




    def __init__(self, Manufacturer, Doors, Model, Year, Price, Body_Type, Transmission, Fuel, Color, Mileage, Reg, URL):
        # Define instance variables
        self.Manufacturer = str(Manufacturer)
        self.Model = str(Model)
        self.Year = int(Year)
        self.Price = int(Price)
        self.Body_Type = str(Body_Type)
        self.Transmission = str(Transmission)
        self.Fuel = str(Fuel)
        self.Color = str(Color)
        self.Mileage = str(Mileage)
        self.Doors = int(Doors)
        self.Reg = str(Reg)
        self.URL = str(URL)


    # Create a table to store used car information if it doesn't exist
    def create_table(self):
        """
        Creates the 'used_cars' table if it doesn't exist.
        The table has columns: id, make, model, and price.
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
                "URL": self.URL
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
                "URL": self.URL
            }
        ]
        self.cursor.execute("select * from used_cars")# Improvement to add table by date
        existing_data = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        reg_col_index = column_names.index('Reg')
 
        for data in incoming_data:
            matching_car = next((car for car in existing_data if (car[reg_col_index]) == (data["Reg"])), None)
            if(matching_car):
                print(f"Car with REG: {matching_car[reg_col_index]} is existing. Not adding.")
            else: # Add a car into database
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
batchofcarsimport = sqlite_database(
    Body_Type="Hatch",
    Color="Black",
    Fuel="Diesel",
    Doors=5,
    Manufacturer="Ford",
    Mileage=66000,
    Model="Fiesta",
    Price=12000,
    Reg="2mk60g22",
    Year=2017,
    Transmission="Manual",
    URL="www.google.com"
)
batchofcarsimporttest = sqlite_database(
    Body_Type="Hatch",
    Color="Black",
    Fuel="Diesel",
    Doors=5,
    Manufacturer="Ford",
    Mileage=66000,
    Model="Focus",
    Price=12000,
    Reg="2mk60g22",
    Year=2017,
    Transmission="Manual",
    URL="www.google.com"
)

batchofcarsimport.create_table()  # Create the 'used_cars' table if it doesn't exist
#Import car data
batchofcarsimport.import_data()
batchofcarsimporttest.import_data()





batchofcarsimport.retrieve_db(column="price", input_data=100000)
batchofcarsimport.retrieve_db(column="color", input_data='black')
batchofcarsimport.retrieve_db(column="doors", input_data='5')


batchofcarsimport.close_db()  # Close the database connection and cursor