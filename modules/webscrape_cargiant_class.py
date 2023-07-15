from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import requests

class webscrape_cargiant():
    date_retrieved = datetime.time()
    driver = None
    



    def __init__(self, driver, keepalive, manufacturer_search=None ):
        self.driver = str(driver)
        self.keepalive = bool(keepalive)
        self.data = pd.DataFrame()
        self.length = self.data.shape[0]
        if manufacturer_search is not None:
            self.manufacturer_search = manufacturer_search
            self.url = "https://www.cargiant.co.uk/search/" + manufacturer_search + "/all"
            print("Setting the search to", self.url)
        else: 
            self.url = "https://www.cargiant.co.uk/search/all/all"
    def initialize_driver(self):
        if(self.driver == "safari"):
           
            safari_options = SafariOptions()
            safari_options.headless = True  # Safari doesn't support the "--headless" argument, so we use the headless property

            webscrape_cargiant.driver = webdriver.Safari(safari_options)

        elif(self.driver == "chrome"):
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1200")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--start-minimized")

            webscrape_cargiant.driver = webdriver.Chrome(options=chrome_options)
    
        elif(self.driver == "firefox"):
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            firefox_options.add_argument("--window-size=1920,1200")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--start-minimized")
            webscrape_cargiant.driver  = webdriver.Firefox(options=firefox_options)

    def searchForManufacturer(self, Manufacturer):
        self.manufacturer_search = Manufacturer
        self.url = "https://www.cargiant.co.uk/search/" + Manufacturer + "/all"
        print("Setting the search to", self.url)
        self.pullNewData()

    def import_sqldb_data(self, DataFrame):
        print("Importing past DATA")
        self.data = DataFrame
        

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
        print(self.url)
        self.initialize_driver()
        # Set up the Selenium Webwebscrape_cargiant.driver
        # Send a GET request to the website
        # Replace with the URL of the website you want to scrape
        wait = WebDriverWait(webscrape_cargiant.driver, 10) 
        webscrape_cargiant.driver.get(self.url)
        # Adjust the timeout value as needed
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.car-listing-item")))

        soup = BeautifulSoup(webscrape_cargiant.driver.page_source, 'html.parser')

        car_listing_items = webscrape_cargiant.driver.find_elements(
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
            "Reg": [],
            "URL": []
        }

    
        tf = pd.DataFrame(tableTemplate)
        
        # Create a table containing the objects
        for item in car_listing_items:
            # Process each car listing item
            price_get = item.find_element(By.CSS_SELECTOR, "div.price-block__price").text
            price = re.sub("[^0-9.]","", price_get)
            model = item.find_element(By.CSS_SELECTOR, "span.title__main.set-h3").text
            model_split = re.split(r'(^\s*[\w]+)\b', model)
            model_split = [item for item in model_split if item]
            car_manufacturer = model_split[0]
            model_name = model_split[1].strip()
 
            year_get = item.find_element(
                By.CSS_SELECTOR, "span.title__sub__plate").text.replace(",", "")
            year = re.sub(r"(\d{4}).*", r"\1" , year_get)
            link = item.find_element(By.CSS_SELECTOR, "a.car-listing-item__details.split-half")
            carLink = link.get_attribute("HREF")
            carReg = (re.split(r"[/\\](?=[^/\\]*$)", carLink))[1]
            #  split string details into the correct specs
            details = item.find_element(
                By.CSS_SELECTOR, "span.text-content").text.strip()
            details_split = details.split(', ')
            DoorsAndType, Transmission, Fuel, Color, mileage_get = details_split
            mileage = re.sub("[^0-9.]", "" , mileage_get)
            

            # Also split the door and body type
            DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)
            
            #Empty strings to initalize
            number_doors = ""
            bodyType = ""
            for item in DoorsAndType_split:
                if (re.match(r'\d', item)):
     
                    number_doors, bodyType = re.split(r'(?<=\d)\s...', item)
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
                "URL": carLink,
                "Reg": carReg
            }

            i = len(tf) + 1
            tf.loc[i] = NewRow
        if self.data.empty:
            print("Table is empty or has columns")
            self.data = tf
        else:
            print("table already has data")
            self.data = pd.concat([self.data.reset_index(drop=True), tf.reset_index(drop=True)] )
            print(tf)

        if(self.keepalive == False):
            webscrape_cargiant.driver.quit()
        print("Data successfully pulled")