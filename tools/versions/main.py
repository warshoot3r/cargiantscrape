from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

# Set up the Selenium WebDriver
driver = webdriver.Safari()

# Send a GET request to the website
# Replace with the URL of the website you want to scrape
url = 'https://www.cargiant.co.uk/search/bmw/all'

webpage = driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

car_listing_items = driver.find_elements(
    By.CSS_SELECTOR, "div.car-listing-item")

# Create Pandas table
tableTemplate = {
    "Manufacturer": [],
    "Model": [],
    "Year": [],
    "Price": [],
    "Body Type": [],
    "Tranmission": [],
    "Fuel": [],
    "Color": [],
    "Mileage": [],
    "Doors": [],
    "URL": []
}


tf = pd.DataFrame(tableTemplate)

# Create a table containing the objects
for item in car_listing_items:
    # Process each car listing item
    price = item.find_element(By.CSS_SELECTOR, "div.price-block__price").text
    model = item.find_element(By.CSS_SELECTOR, "span.title__main.set-h3").text
    model_split = re.split(r'(^\s*[\w]+)\b', model)
    model_split = [item for item in model_split if item]
    car_manufacturer = model_split[0]
    model_name = model_split[1]
    details = item.find_element(
        By.CSS_SELECTOR, "span.text-content").text.strip()
    year = item.find_element(
        By.CSS_SELECTOR, "span.title__sub__plate").text.replace(",", "")
    link = item.find_element(By.CSS_SELECTOR, "a.car-listing-item__details.split-half")
    carLink = link.get_attribute("HREF")
    #  split string details into the correct specs
    details_split = details.split(', ')
    DoorsAndType, Transmission, Fuel, Color, mileage = details_split

    # Also split the door and body type
    DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)
    
    #Empty strings to initalize
    number_doors = ""
    bodyType = ""
    for item in DoorsAndType_split:
         if (re.match(r'\d', item)):
            number_doors, bodyType= item.split(" ", 1)
         else:
             bodyType = item
      
    # If no doors variable, change it empty
    if(not(number_doors)):
       number_doors = "N/A"

    NewRow = {
        "Manufacturer": car_manufacturer,
        "Model": model_name,
        "Year": year,
        "Details": details,
        "Price": price,
        "Body Type": bodyType,
        "Doors": number_doors,
        "Tranmission": Transmission,
        "Fuel": Fuel,
        "Color": Color,
        "Mileage": mileage,
        "URL": carLink
    }

    i = len(tf) + 1
    tf.loc[i] = NewRow


print(tf)
driver.quit()
