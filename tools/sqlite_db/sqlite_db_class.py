import sqlite3

# Connect to a database or create one if it doesn't exist
conn = sqlite3.connect('used_cars.db')
cursor = conn.cursor()


# Create a table to store used car information if it doesn't exist
def create_table():
    """
    Creates the 'used_cars' table if it doesn't exist.
    The table has columns: id, manufacturer, model, and price.
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS used_cars
               (id INTEGER PRIMARY KEY, manufacturer TEXT, model TEXT, price INTEGER)''')


# Print all information from the 'used_cars' table
def print_all_table():
    """
    Prints all the data in the 'used_cars' table.
    """
    print("Printing table information:")
    cursor.execute("SELECT * from used_cars")
    for item in cursor.fetchall():
        print(item)


# Import car data into the 'used_cars' table
def import_data(manufacturer, model, price):
    """
    Imports car data into the 'used_cars' table.
    If a car already exists, it checks if the price has changed.
    """
    incoming_data = [{'manufacturer': manufacturer, 'model': model, 'price': price}]
    cursor.execute("SELECT * from used_cars")
    existing_data = cursor.fetchall()

    for data in incoming_data:
        matching_car = next((car for car in existing_data if car[1] == data['manufacturer'] and car[2] == data['model']), None)

        if matching_car:
            if matching_car[3] != data['price']:
                print(f"Price changed for {data['manufacturer']} {data['model']}: {matching_car[3]} -> {data['price']}")
        else:
            cursor.execute("INSERT INTO used_cars(manufacturer, model, price) VALUES (?,?,?)", (data['manufacturer'], data['model'], data['price']))
            print(f"New car added: {data['manufacturer']} {data['model']}")
    conn.commit()


def retrieve_db(column, input_data):
    if(column == "price"):
       command = f"SELECT * from used_cars where {column} <= {input_data} "
    else: 
       command = f"SELECT * from used_cars where {column} = {input_data} "
    cursor.execute(command)
    data = cursor.fetchall()
    print(f"\nPrinting data from query: {column} -> {input_data}")
    for item in data: print(item)


# Close the database connection and cursor
def close_db():
    """
    Closes the database connection and cursor.
    """
    cursor.close()
    conn.close()


# Main program execution
create_table()  # Create the 'used_cars' table if it doesn't exist
print_all_table()  # Print all data from the 'used_cars' table
import_data(price=10000, model="Corolla", manufacturer="Toyota")  # Import car data
import_data(price=90000, model="Fiesta", manufacturer="Ford")  # Import car data
retrieve_db(column="price", input_data=10000)
close_db()  # Close the database connection and cursor
