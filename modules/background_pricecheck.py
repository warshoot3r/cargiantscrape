import bs4
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chromium.options import ChromiumOptions as ChromiumOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import concurrent.futures
class car:
    def __init__(self, reg: str, car_make: str, car_model: str, mileage: int, year: int):
        self.reg = reg
        self.car_make = car_make
        self.car_model = car_model
        self.mileage = mileage
        self.year = year
        self.autotrader_price_valuation = None
    
    def __str__(self):
        return f"Registration: {self.reg}\nMake: {self.car_make}\nModel: {self.car_model}\nMileage: {self.mileage} miles\nYear: {self.year}"


class car_background_information:
    def __init__(self, driver: str, postal_code: str):
        self.cars = {}
        self.driver = driver
        self.postal_code = postal_code
    def selenium_setup(self):
        if self.driver == "safari":
            safari_options = SafariOptions()
            return webdriver.Safari(options=safari_options)
        
        elif self.driver == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1200")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-minimized")
            return webdriver.Chrome(options=chrome_options)
        elif self.driver == "chromium":
            chromium_options = ChromiumOptions()
            chromium_options.add_argument("--no-sandbox")
            chromium_options.add_argument("headless")
            chromium_options.add_argument("--crash-dumps-dir=/tmp")
            chromium_options.add_argument("--disable-gpu")
            chromium_options.add_argument("--disable-dev-shm-usage")
            chromium_options.add_argument("--window-size=800,600")
            chromium_options.add_argument("--ignore-certificate-errors")
            chromium_options.add_argument("--disable-extensions")
            chromium_options.add_argument("--start-minimized")
            return webdriver.Chrome(options=chromium_options)
       
        elif self.driver == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            firefox_options.add_argument("--window-size=1920,1200")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--start-minimized")
            return webdriver.Firefox(options=firefox_options)
    def get_all_cars(self):
        return self.cars.items()
    
    def add_car(self, car: car):
        print(f"Imported Car {car.reg}")
        self.cars[car.reg] = car
        

    def get_car_properties(self, reg) -> car:
        car = self.cars.get(reg, None)
        return car 
    
    def get_autotrader_prices(self, reg):
        """
        returns a list of prices scraped from autotrader
        """
        return self.cars.get(reg, None).autotrader_price_valuation
    
    def get_car_percentage_range(self, reg, price_to_check):
        """
        Must call get_autotrader_prices first
        ARGS 
        price of car
       
        Returns a int representing the percentage between the values.
        """
        prices = self.cars.get(reg, None).autotrader_price_valuation
        if prices is None or (len(prices) < 2) :
            return
        prices_as_int = [int(value.replace(',', '' )) for value in prices]

        upper_bound  = max(prices_as_int)
        lower_bound = min(prices_as_int)
        percentage_range = (price_to_check - lower_bound)/ (upper_bound - lower_bound ) * 100
    
        return int(percentage_range)



    def get_car_range_price(self, reg):

        """
        returns a str with a range of high and low prices
        """
        
        prices = self.cars.get(reg, None).autotrader_price_valuation
        if (prices is None) or (len(prices) < 2):
            return
        prices_as_int = [int(value.replace(',', '' )) for value in prices]

        max_price = max(prices_as_int)
        min_price = min(prices_as_int)
        return "£" + str(min_price)  + (" - ") + "£" +  str(max_price)
    
    def parallel_scrape_autotrader_price(self, worker_threads=2):
                """
                concurrently pull prices from autotrader
                
                Returns:
                    Nothing
                
                """
                #parallel processes
                with concurrent.futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
                    futures = []
                    for car in self.cars.items():
                        #array 0 is the reg. array 1 contains the params
                        car_make = car[1].car_make
                        car_model = car[1].car_model
                        mileage = car[1].mileage
                        year = car[1].year
                        reg = car[1].reg
        
                        #patching values for autotrader 
                        if(car_make == "Mercedes"):
                            car_make = "Mercedes-Benz"
                        
                        future = executor.submit(self.scrape_autotrader, car_make, car_model, mileage, year, reg)
                        futures.append(future)
                    concurrent.futures.wait(futures)

    def scrape_autotrader(self, car_make, car_model, mileage, year, reg):
            # Navigate to the URL
            driver = self.selenium_setup()
            wait = WebDriverWait(driver, timeout=5)
            print(f"Trying to scrape {reg}", flush=True)

            minimum_mileage = mileage - 3000
            maximum_mileage = mileage + 3000
            from_year = year - 1
            to_year = year
            #try twice by changing the models:
            attempts_max = 3
            attempts = 0

            #convert spaces in string for http friendly url
            car_model = car_model.replace(" ", "%20")
            # Define the URL
            car_parameters = f"&make={car_make}",f"&aggregatedTrim={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
            temp = "".join(car_parameters)
            autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp

         
            while attempts < attempts_max:
                try:     #Error basic handling None and not 200
                    print(f"Attempt {attempts}", flush=True)
                    print(f"DEBUG: url='{autotrader}'", flush=True)
                    driver.get(autotrader)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="advertCard"]')))


                except exceptions.TimeoutException:
                    attempts +=1
                    if attempts == 1:
                        car_model = str(car_model).lower()
                        print("trying in lowercase",flush=True)
                        car_parameters = f"&make={car_make}",f"&aggregatedTrim={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
                        temp = "".join(car_parameters)
                        autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp
                    elif attempts == 2:
                        print(f"Page did not load. Empty page")        
                        print("Switching from \"aggregated body\" to \"model\" and restarting")
                        car_parameters = f"&make={car_make}",f"&model={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
                        temp = "".join(car_parameters)
                        autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp

                    else:
                        print("Not able to get prices", flush=True)
                        
                    
            data = driver.page_source

            # Parse the HTML content with BeautifulSoup
            bs = bs4.BeautifulSoup(data, features="html.parser")

            # Find the container with car listings
            table_data = bs.find('ul', {'data-testid': 'desktop-search'})

            # Find all individual car listings
            try:
                number_of_cars = table_data.find_all('li')
            except:
                print("No data")
                
            # Define a regular expression pattern to extract prices (£X,XXX.XX format)
            pattern = re.compile(r'£(\d{1,3},\d{3})*(\.\d{2})?')

            # Extract and print prices from car listings

            cars_list = []
            for car in number_of_cars:
                text = car.text.strip()  # Get the text content of the car listing with proper stripping
                matches = pattern.findall(text)
                # Print the matching prices
                for match in matches: # ignoring last two as they are adverts
                    price = ''.join(match)
                    if price:
                        cars_list.append(price)
                        
            print(f"Successfully got prices for {reg}", flush=True)
            self.cars[reg].autotrader_price_valuation = cars_list[:-2]
            driver.close()
            driver.quit()




         

    def scrape_autotrader_price(self):
        """
        Retrieves a price from autotrader based on input values.

        Args:
            car_make: car name eg. Ford
            car_model: car model name eg. Fiesta
            mileage: expected car mileage eg. 50000
            year: expected year eg 2019

        returns a list of prices as int

        """

        #init variables
        
        for car in self.cars.items():
            car_make = car[1].car_make 
            car_model = car[1].car_model
            mileage = car[1].mileage
            year = car[1].year
            reg = car[1].reg
    

            minimum_mileage = mileage - 3000
            maximum_mileage = mileage + 3000
            from_year = year - 1
            to_year = year
            

            
            driver = self.selenium_setup()
            # Wait for the presence of the advert cards
            wait = WebDriverWait(driver, timeout=5)

            #patching values for autotrader 
            if(car_make == "Mercedes"):
                car_make = "Mercedes-Benz"

            #convert spaces in string for http friendly url
            car_model = car_model.replace(" ", "%20")
            # Define the URL
            car_parameters = f"&make={car_make}",f"&aggregatedTrim={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
            temp = "".join(car_parameters)
            autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp

         
            # Navigate to the URL

            #try twice by changing the models:
            attempts_max = 3
            attempts = 0
            while attempts < attempts_max:
                try:     #Error basic handling None and not 200
                    print(f"Attempting {attempts}")
                    print(f"DEBUG: url='{autotrader}'", flush=True)
                    driver.get(autotrader)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="advertCard"]')))
                    break

                except exceptions.TimeoutException:
                    attempts +=1
                    if attempts == 1:
                        car_model = str(car_model).lower()
                        print("trying in lowercase")
                        car_parameters = f"&make={car_make}",f"&aggregatedTrim={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
                        temp = "".join(car_parameters)
                        autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp
                    elif attempts == 2:
                        print(f"Page did not load. Empty page")        
                        print("Switching from \"aggregated body\" to \"model\" and restarting")
                        car_parameters = f"&make={car_make}",f"&model={car_model}",f'&minimum-mileage={minimum_mileage}',f'&maximum-mileage={maximum_mileage}', f'&year-from={from_year}', f'&year-to={to_year}'
                        temp = "".join(car_parameters)
                        autotrader = f"https://www.autotrader.co.uk/car-search?postcode={self.postal_code}" + temp

                    else:
                        print("Not able to get prices")
                        break
                    
            data = driver.page_source

            # Parse the HTML content with BeautifulSoup
            bs = bs4.BeautifulSoup(data, features="html.parser")

            # Find the container with car listings
            table_data = bs.find('ul', {'data-testid': 'desktop-search'})

            # Find all individual car listings
            try:
                number_of_cars = table_data.find_all('li')
            except:
                print("No data")
                break
                
            # Define a regular expression pattern to extract prices (£X,XXX.XX format)
            pattern = re.compile(r'£(\d{1,3},\d{3})*(\.\d{2})?')

            # Extract and print prices from car listings

            cars_list = []
            for car in number_of_cars:
                text = car.text.strip()  # Get the text content of the car listing with proper stripping
                matches = pattern.findall(text)
                # Print the matching prices
                for match in matches: # ignoring last two as they are adverts
                    price = ''.join(match)
                    if price:
                        cars_list.append(price)
                        break
            print(f"Successfully got prices for {reg}", flush=True)
            self.cars[reg].autotrader_price_valuation = cars_list[:-2]


# ## example

# #set up 
# car_db = car_background_information(driver="chrome")


# #import a car
# james_car = car("WK60ZTY", "Ford", "Fiesta", 65600, 2010)
# car_db.add_car(car=james_car)


# #get price data
# car_db.scrape_autotrader_price()


# #print the prices
# print(car_db.get_autotrader_prices(reg="WK60ZTY"))

# #print the range prices
# print(car_db.get_car_range_price(reg="WK60ZTY"))

