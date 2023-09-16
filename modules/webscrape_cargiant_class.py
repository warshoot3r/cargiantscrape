from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chromium.options import ChromiumOptions as ChromiumOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import concurrent.futures
class WebScraperCargiant:
    """
    A web scraper for collecting used car information from the Cargiant website.
    """

    driver = None
    
    def __init__(self, driver, keepalive, manufacturer_search=None):
        """
        Initializes the WebScraperCargiant object.

        Args:
            driver (str): The driver type to use for Selenium (safari, chrome, or firefox).
            keepalive (bool): Determines whether to keep the driver alive after data retrieval.
            manufacturer_search (str, optional): The manufacturer to search for. Defaults to None.
        """
        self.driver = str(driver)
        self.keepalive = bool(keepalive)
        self.data = pd.DataFrame()
        pd.set_option("display.max_colwidth", 100)
        self.length = self.data.shape[0]
        if manufacturer_search is not None:
            self.manufacturer_search = manufacturer_search
            self.url = "https://www.cargiant.co.uk/search/" + manufacturer_search + "/all"
            print("Setting the search to", self.url)
        else: 
            self.url = "https://www.cargiant.co.uk/search/all/all"

    def initialize_driver(self):
        """
        Initializes the Selenium driver based on the specified driver type.
        """
        if self.driver == "safari":
            safari_options = SafariOptions()
            safari_options.headless = True  # Safari doesn't support the "--headless" argument, so we use the headless property
            return webdriver.Safari(options=safari_options)
        
        elif self.driver == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.headless = True
            chrome_options.add_argument("--headless")
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

    def print_number_of_cars(self):
        """
        Prints the number of cars scraped from cargiant
        """
        print(f"\n\nNumber of cars scraped from cargiant -> {self.length}\n\n")

    def search_for_manufacturer(self, manufacturer, numberofpages=5):
        """
        Sets the search to a specific manufacturer. This does not save the generic model eg, 3 series
        Args:
                manufacturer (str): The manufacturer to search for.
                NumberOfPages(int): Defines how many pages to scrape
        Return:
                pull_new_data returns a panda table`

        """
        self.numberofpages = numberofpages
        self.manufacturer_search = manufacturer
        url = "https://www.cargiant.co.uk/search/" + manufacturer + "/all"
        print("Setting the search to", url)
        self.pull_new_data(numberofpages=numberofpages, url=url)

    def search_for_manufacturer_with_bmw_or_mercedes(self, manufacturer, numberofpages=10 ):
        """
        Parallel pull. Sets the search to a specific manufacturer. This will save the generic model as "https://www.cargiant.co.uk/search/" + manufacturer "HERE" the  eg, 3 series
        Args:
                manufacturer (str): The manufacturer to search for.
                NumberOfPages(int): Defines how many pages to scrape
        Return:
                pull_new_data returns a panda table`

        """
        self.manufacturer_search = manufacturer
        if not(manufacturer == "BMW") and not(manufacturer == "Mercedes"):
            raise TypeError("Must be BMW or Mercedes")
        if manufacturer == "BMW":
            series = ["all-1-series", "all-2-series", "all-3-series", "all-4-series", "all-5-series", "all-6-series", "all-7-series"]
        elif manufacturer == "Mercedes":
            series = ["all-a-class", "all-b-class", "all-c-class", "all-e-class", "all-s-class"]
        
        self.parallel_pull_new_data(manufacturer=manufacturer, series_to_process=series, number_of_pages=numberofpages)
        return self.data
    def import_sqldb_data(self, data_frame):
        """
        Imports past data from a DataFrame.

        Args:
            data_frame (pd.DataFrame): The DataFrame containing past data to be imported.
        """
        print("Importing past data", flush=True)
        self.data = data_frame

    def get_car_makes(self):
        """
        Prints the list of car makes available on the Cargiant website.
        """
        driver = requests.get("https://www.cargiant.co.uk/search/")
        content = driver.content
        soup = BeautifulSoup(content, 'html.parser')
        makes = soup.find_all(id="Makes")
        print("Listing Car makes", flush=True)
        for item in makes:
            print(item.text)


    def search_data_for_car(self, search_col, term):
        """
        Searches the data for a specific car based on the specified column and term.

        Args:
            search_col (str): The column name to search for.
            term (str): The term to be searched in the specified column.

        Returns:
            WebScraperCargiant: A new WebScraperCargiant object containing the search results.
        """
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

    def pull_new_data(self, url, numberofpages=10):
    
        """
        Retrieves new car data from the Cargiant website and updates the DataFrame.

        """
        print(f"Pulling new data: {url}", flush=True)
        driver = self.initialize_driver()
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.car-listing-item")))
        car_listing_items_page_1 = driver.find_elements(By.CSS_SELECTOR, "div.car-listing-item")
        self.extract_web_data(car_listing_items_page_1)
        # check if only 1 page here. we must stop if is only one. otherwise code below will scrape same page.
        page_count = driver.find_element(By.CSS_SELECTOR, "#TotalPages").get_attribute("value")#

        if page_count == "1":
            print(f"Stopping scraping as only 1 page")
        
        else:
            for page in range(1,numberofpages+1):
                pages = driver.find_elements(By.CSS_SELECTOR , '[data-paging-pages-template="page"]')
                print(f"Currently web scraping {self.manufacturer_search} cars on page {page+1}.")
                try:
                    driver.execute_script("arguments[0].click()", pages[page]) # click page
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.car-listing-item")))
                    current_page = driver.find_elements(By.CSS_SELECTOR, "div.car-listing-item")
                    self.extract_web_data(current_page)
                    print("Page successfully scraped", flush=True)
                except IndexError:
                    print("No more pages to scrape", flush=True)
                    return
        self.stopwebdriver(driver)
   
    def extract_web_data(self, scraped_data):
        
       
        table_template = {
            "Manufacturer": [],
            "Car Status": [],
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

        tf = pd.DataFrame(table_template)
        
        for item in scraped_data:
            # Extracting car details
            price_get = item.find_element(By.CSS_SELECTOR, "div.price-block__price").text
            price = re.sub("[^0-9.]", "", price_get)
            model = item.find_element(By.CSS_SELECTOR, "span.title__main.set-h3").text
            model_split = re.split(r'(^\s*[\w]+)\b', model)
            model_split = [item for item in model_split if item]
            car_manufacturer = model_split[0]
            model_name = model_split[1].strip()

            year_get = item.find_element(By.CSS_SELECTOR, "span.title__sub__plate").text.replace(",", "")
            year = re.sub(r"(\d{4}).*", r"\1" , year_get)
            link = item.find_element(By.CSS_SELECTOR, "a.car-listing-item__details.split-half")
            car_link = link.get_attribute("HREF")
            car_reg = (re.split(r"[/\\](?=[^/\\]*$)", car_link))[1]

            details = item.find_element(By.CSS_SELECTOR, "span.text-content").text.strip()
            details_split = details.split(', ')
            DoorsAndType, Transmission, Fuel, Color, mileage_get = details_split
            mileage = re.sub("[^0-9.]", "" , mileage_get)
            try:
                car_status_get =  item.find_element(By.CSS_SELECTOR, "span.caption-block").text
                if(car_status_get == "SOLD TODAY"):
                    car_status = "Sold"
                elif(car_status_get == "RESERVED"):
                    car_status = "Reserved"
                elif(car_status_get == "AVAILABLE"):
                    car_status = "Available"
                else: 
                    car_status = car_status_get
                print(f"VERBOSE: {model_name} saved as {car_status}", flush=True)
            except NoSuchElementException:
                car_status = ""
                print(f"VERBOSE: {model_name} status is empty. {car_status}", flush=True)

            DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)

            number_doors = ""
            body_type = ""
            for item in DoorsAndType_split:
                if re.match(r'\d', item):
                    number_doors, body_type = re.split(r'(?<=\d)\s...', item)
                else:
                    body_type = item
            
            if not number_doors:
                number_doors = "N/A"



            new_row = {
                "Manufacturer": car_manufacturer,
                "Model": model_name,
                "Year": year,
                "Details": details,
                "Price": price,
                "Body Type": body_type,
                "Doors": number_doors,
                "Transmission": Transmission,
                "Fuel": Fuel,
                "Color": Color,
                "Mileage": mileage,
                "URL": car_link,
                "Reg": car_reg,
                "Car Status": car_status
            }

            i = len(tf) + 1
            tf.loc[i] = new_row
        
        if self.data.empty:
            print("VERBOSE: No existing data. Scraped data is database ")
            self.data = tf
            self.length = tf.shape[0]
        else:
            self.data = pd.concat([self.data.reset_index(drop=True), tf.reset_index(drop=True)])
            print("VERBOSE: Appended to self.data ")
            self.length = self.data.shape[0]
            print("Saved to database and returning this scrape as pd.")
           
        # if not self.keepalive:
        #     driver.quit()
        
        print(f"Data successfully pulled {tf.shape[0] } cars")
    def parallel_pull_new_data(self, series_to_process, manufacturer=None, number_of_pages=7, worker_threads=4):
            """
            concurrently pull cargiant cars with multiple urls. 
            "https://www.cargiant.co.uk/search/"+  manufacturer + "/" + series_name
            
            Inputs:
                - manufactuere type(str) eg. BMW
                - series name  type(array) eg. all-1-series
                - worker threads = number of parallel workers scraping at same time
            URL is created to be an array like https://www.cargiant.co.uk/search/BMW/all-6-series

            Returns:
                database
            
            """
            
            with concurrent.futures.ThreadPoolExecutor(worker_threads) as executor:
                futures = []

                for series_name in series_to_process:
                    url = "https://www.cargiant.co.uk/search/"+  manufacturer + "/" + series_name
                    future = executor.submit(self.pull_new_data, url, number_of_pages)
                    futures.append(future)

                # Wait for all futures to complete
                concurrent.futures.wait(futures)

                # If you want to access the results from the futures, you can iterate through futures and retrieve results
                for future in futures:
                    result = future.result()
                    print(f"Finished a {result} scrape")
                    print(result)
                    # Process the result as needed
        
    def stopwebdriver(self, driver):
        """
        Closes the browser and Kills the web driver.
        """
        driver.close()
        driver.quit()
        #Force killing the processes
    def check_reg_url_alive(self, Registration):
        """
        Returns true if reg url is alive. Used with DB to move to sold database
        Args:
        takes a single variable URL(str) eg. https://www.cargiant.co.uk/car/Lexus/CT-200h/YD67PCX
        """

        # check if car giant is alive 
        main_website = requests.get("https://www.cargiant.co.uk")
        if main_website.ok:
            get_reg_url = requests.get(Registration)
            if get_reg_url.url == "https://www.cargiant.co.uk/":
                print(f"Link return {get_reg_url.url}. {Registration} likely sold.")
                return True
            else:
                print(f"{Registration} is not sold . Nothing to do")
                return False
            
        else:
            return ConnectionRefusedError
