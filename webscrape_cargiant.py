from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import requests

class webscrape_cargiant():
    url = "https://www.cargiant.co.uk/search/"
    manufacturer = ""
    date_retrieved = datetime.time()
    data = pd.DataFrame()

    def __init__(self, manufacturer_search=None ):
        if manufacturer_search is not None:
            self.manufacturer_search = manufacturer_search
            self.url = "https://www.cargiant.co.uk/search/" + manufacturer_search + "/all"
            print("Setting the search to", self.url)
            self.pullNewData()

    def getCarMakes_selenium(self): # Avoid using as resource hogging
        driver = webdriver.Safari()
        driver.get("https://www.cargiant.co.uk/search/")
        makes = driver.find_elements(By.ID, "Makes")
        for item in makes:
            print(item.text)

    def getCarMakes(self):
        driver = requests.get("https://www.cargiant.co.uk/search/")
        content = driver.content
        soup = BeautifulSoup(content, 'html.parser')
        makes = soup.find_all(id="Makes")
        print("Listing Car makes")
        for item in makes:
            print(item.text)
        
    def printData(self):
        print("Printing data")
        print(self.data)
        print(self.date_retrieved)


    def searchDataForCar(self, search_col, term):
        if search_col not in self.data.columns.values:
            print(f"{search_col} must be one of:")
            print(self.data.columns.values)
            return
        pattern = re.escape(term)
        mask = self.data[search_col].apply(lambda x: bool(re.search(pattern, x)))
        model_retrieved = self.data[mask]
        
        print(f"\n\nReturning a search with: {search_col} -> {term}")
        print(model_retrieved)
        
        self.data = model_retrieved
        return self

    def pullNewData(self):
        print("Pull new data")
        # Main code to pull data
        
        # Set up the Selenium WebDriver
        driver = webdriver.Safari()

        # Send a GET request to the website
        # Replace with the URL of the website you want to scrape
        url = self.url

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
            "Transmission": [],
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
            model_name = model_split[1].strip()
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
                "Transmission": Transmission,
                "Fuel": Fuel,
                "Color": Color,
                "Mileage": mileage,
                "URL": carLink
            }

            i = len(tf) + 1
            tf.loc[i] = NewRow
        self.data = tf
        driver.quit()
        print("Data successfully pulled")
        # Set time that we retrieved
        self.date_retrieved = datetime.datetime.now()


